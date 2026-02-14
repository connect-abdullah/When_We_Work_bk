from fastapi import APIRouter, Depends, HTTPException, status
from app.entities.user.service import UserService
from app.entities.user.schema import ForgotPassword, UserCreate, UserRead, UserCreateResponse, UserUpdate, UserUpdateByWorker, UserUpdateByAdmin, UserLogin, UserTokenResponse
from app.core.response import APIResponse, ok, fail
from app.core.auth import get_current_admin_id, get_current_admin_id_optional, get_current_worker_id
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.entities.user.modal import UserRoleEnum

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Create User (admin can be created without auth for bootstrap; worker requires admin token)
@router.post("", response_model=APIResponse[UserCreateResponse])
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    admin_id: int | None = Depends(get_current_admin_id_optional),
):
    """Create a user. Admin: no auth needed (for first admin). Worker: requires admin Bearer token."""
    try:
        if user.user_role == UserRoleEnum.admin:
            new_user = UserService(db).create_user(user)
            return ok(data=new_user, message="Admin Created Successfully")
        elif user.user_role == UserRoleEnum.worker:
            if admin_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
            new_user = UserService(db).create_user(user, admin_id=admin_id)
            return ok(data=new_user, message="Worker Created Successfully")
        else:
            return fail(message="Invalid user role")
    except Exception as e:
        return fail(message=str(e))

# Get User by ID
@router.get("/{user_id}", response_model=APIResponse[UserRead])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """ Get a user by ID """
    try:
        user = UserService(db).get_user_by_id(user_id)
        return ok(data=user, message="User Retrieved Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get All Workers by Admin
@router.get("", response_model=APIResponse[list[UserRead]])
def get_all_users(db: Session = Depends(get_db), admin_id: int = Depends(get_current_admin_id)):
    """ Get all workers by admin """
    try:
        users = UserService(db).get_all_workers_by_admin(admin_id=admin_id)
        return ok(data=users, message="Workers Retrieved Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Update User by Admin (can change everything including email and user_role) || Also Change Admin Data
@router.put("/admin/{user_id}", response_model=APIResponse[UserRead])
def update_user_by_admin(
    user_id: int, 
    user: UserUpdateByAdmin, 
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id)
):
    """
    Update user by admin. Admin can change everything including:
    - email
    - user_role
    - All other user fields
    - Also Change Admin Data
    """
    try:
        updated_user = UserService(db).update_user(user_id=user_id, payload=user)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return ok(data=updated_user, message="User Updated Successfully by Admin")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))


# Update User by Worker (self-update, cannot change email or user_role)
@router.put("/worker/me", response_model=APIResponse[UserRead])
def update_worker_profile(
    user: UserUpdateByWorker, 
    db: Session = Depends(get_db),
    worker_id: int = Depends(get_current_worker_id)
):
    """
    Workers update their own profile. Cannot change:
    - email (admin-only)
    - user_role (admin-only)
    """
    try:
        updated_user = UserService(db).update_user(user_id=worker_id, payload=user)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return ok(data=updated_user, message="Profile Updated Successfully")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))


# Delete User  
@router.delete("/{user_id}", response_model=APIResponse[bool])
def delete_user(user_id: int, db: Session = Depends(get_db), admin_id: int = Depends(get_current_admin_id)):
    """ Delete a user """
    try:
        deleted_user = UserService(db).delete_user(user_id=user_id)
        return ok(data=deleted_user, message="User Deleted Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Login User
@router.post("/login", response_model=APIResponse[UserTokenResponse])
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """ Login a user """
    try:
        token = UserService(db).login_user(user)
        return ok(data=token, message="Login Successfully")
    except Exception as e:
        return fail(message=str(e))
    
@router.post("/forgot-password", response_model=APIResponse[bool])
def forgot_password(payload: ForgotPassword, db:Session = Depends(get_db)):
    """ Forget Password """
    try:
        response = UserService(db).reset_password(payload)
        return ok(data=response, message="Password successfully sent to email")
    except Exception as e:
        return fail(message=str(e))