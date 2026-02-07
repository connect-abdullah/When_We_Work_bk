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
    Require valid JWT and admin role. Returns admin_id (from token sub).
    Use on routes that require admin (e.g. jobs).
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
        if role != "admin" and role == "worker":
            admin_id = payload.get("admin_id")
            if admin_id is None: 
                raise forbidden_exception
            return admin_id
        elif role != "admin"and role != "worker":
            raise forbidden_exception
        return int(sub)
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