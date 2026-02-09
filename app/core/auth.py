"""
Authentication and Authorization Dependencies

Uses JWT Bearer token. Admin login puts sub=admin_id and role="admin" in the token.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from app.core.security import verify_token
from app.core.logging import get_logger

logger = get_logger(__name__)

security = HTTPBearer()


def get_current_admin_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    STRICT ADMIN ONLY - Returns admin_id (from token sub).
    Use on routes that require admin role for write operations (create/update/delete/approve).
    For viewing jobs that workers should also see, use get_admin_id_for_jobs() instead.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin access required.",
    )
    try:
        token = credentials.credentials
        payload = verify_token(token)
        sub = payload.get("sub")
        role = payload.get("role")
        if sub is None:
            raise credentials_exception
        if role != "admin":
            raise forbidden_exception
        return int(sub)
    except HTTPException:
        raise
    except (InvalidTokenError, ValueError, TypeError) as e:
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception


def get_admin_id_for_jobs(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Returns admin_id for job filtering - works for both admins and workers.
    - If admin: returns their own admin_id (from token sub)
    - If worker: returns their associated admin_id (from token admin_id field)
    
    PURPOSE: Workers need to see jobs posted by their admin, so worker tokens
    contain an admin_id field. This function allows both roles to view jobs
    filtered by admin_id.
    
    SECURITY NOTE: Only use this for READ operations (GET /jobs).
    For CREATE/UPDATE/DELETE, use get_current_admin_id() which is admin-only.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied. Admin or Worker role required.",
    )
    try:
        token = credentials.credentials
        payload = verify_token(token)
        sub = payload.get("sub")
        role = payload.get("role")
        
        if sub is None:
            raise credentials_exception
            
        # Admin: return their own ID
        if role == "admin":
            return int(sub)
            
        # Worker: return their associated admin_id from token
        if role == "worker":
            admin_id = payload.get("admin_id")
            if admin_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Worker token missing admin_id field",
                )
            return int(admin_id)
            
        # Any other role is forbidden
        raise forbidden_exception
        
    except HTTPException:
        raise
    except (InvalidTokenError, ValueError, TypeError) as e:
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception


def get_current_admin_id_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
) -> int | None:
    """Return admin_id from JWT if valid admin token present, else None. Use for routes that allow optional admin auth."""
    if credentials is None:
        return None
    try:
        token = credentials.credentials
        payload = verify_token(token)
        sub = payload.get("sub")
        role = payload.get("role")
        if sub is not None and role == "admin":
            return int(sub)
    except Exception:
        pass
    return None

def get_current_worker_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """Return worker_id from JWT if valid worker token present, else raises. Use for routes that require worker auth."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    forbidden_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Worker access required.",
    )
    try:
        token = credentials.credentials
        payload = verify_token(token)
        sub = payload.get("sub")
        role = payload.get("role")
        if sub is None:
            raise credentials_exception
        if role != "worker":
            raise forbidden_exception
        return int(sub)
    except HTTPException:
        raise
    except (InvalidTokenError, ValueError, TypeError) as e:
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception