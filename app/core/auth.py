"""
Authentication and Authorization Dependencies

This module follows FastAPI's official OAuth2 with JWT pattern.
Reference: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

Usage:
- get_current_user: Extract authenticated user from JWT token (dependency)
- require_admin: Ensure user has admin role (dependency)
- require_vendor_or_admin: Ensure user has vendor/admin role (dependency)
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from app.core.security import verify_token
from app.core.logging import get_logger
from app.db.postgres import get_db
from app.models.user import User, UserRoleEnum
from app.schemas.user import UserRead

logger = get_logger(__name__)

# Simple Bearer token extraction from Authorization header
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserRead:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Extract token from Bearer credentials
        token = credentials.credentials
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        # Convert user_id to int (it's stored as string in JWT)
        logger.info(f"User ID: {user_id}")
        user_id = int(user_id)
    except HTTPException:
        # Re-raise HTTPException from verify_token (expired, invalid, etc.)
        raise
    except (InvalidTokenError, ValueError, TypeError) as e:
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception
    
    # Retrieve user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return UserRead.model_validate(user)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserRead:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Extract token from Bearer credentials
        token = credentials.credentials
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        # Convert user_id to int (it's stored as string in JWT)
        logger.info(f"User ID: {user_id}")
        user_id = int(user_id)
    except HTTPException:
        # Re-raise HTTPException from verify_token (expired, invalid, etc.)
        raise
    except (InvalidTokenError, ValueError, TypeError) as e:
        logger.error(f"Token validation error: {str(e)}")
        raise credentials_exception
    
    # Retrieve user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user_id


def require_worker_id(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    """
    Ensure current user has WORKER role.
    """
    if current_user.role != UserRoleEnum.WORKER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required. Only customers can perform this operation."
        )
    return current_user.id


def require_admin_id(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    """
    Ensure current user has ADMIN role.
    """
    if current_user.role != UserRoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required. Only admins can perform this operation."
        )
    return current_user.id

def require_admin(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    """
    Ensure current user has MANAGER or ADMIN role.
    
    MANAGER/ADMIN users can:
    - Manage business operations
    - Create/edit services and categories
    - Manage staff and customers
    - View business analytics
    
    Raises:
        HTTPException 403: User lacks management privileges
    """
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.VENDOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor or Admin access required for business operations."
        )
    return current_user



# Convenience dependencies for common access patterns
get_current_admin_id = require_admin_id
get_current_admin = require_admin