from fastapi import APIRouter, Depends, HTTPException, status
from app.entities.user.service import UserService
from app.entities.user.schema import UserCreate, UserRead, UserCreateResponse, UserUpdate, UserLogin, UserTokenResponse
from app.core.response import APIResponse, ok, fail
from app.core.auth import get_current_admin_id, get_current_admin_id_optional
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
    
# Update User
@router.put("/{user_id}", response_model=APIResponse[UserRead])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """ Update a user """
    try:
        updated_user = UserService(db).update_user(user_id=user_id, payload=user)
        return ok(data=updated_user, message="User Updated Successfully")
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