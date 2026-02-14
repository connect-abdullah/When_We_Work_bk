from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from app.entities.user.modal import UserRoleEnum, Gender, EmploymentType    

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str | None = None
    emergency_contact: str | None = None
    photo: str | None = None
    gender: Gender
    availability: bool = True
    employment_type: EmploymentType | None = None

    user_role: UserRoleEnum | None = None
    worker_roles: list[str] | None = None # worker roles are the roles that the user can perform
    remarks: str | None = None
    
class UserCreate(UserBase):
    admin_id: int | None = None
    business_id: int | None = None
    password: str | None = None
    pass

class UserUpdateByWorker(BaseModel):
    """
    Worker self-update schema - workers can update their own info.
    CANNOT change: email, user_role (admin-only fields)
    """
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    photo: str | None = None
    gender: Gender | None = None
    availability: bool | None = None
    password: str | None = None
    employment_type: EmploymentType | None = None
    worker_roles: list[str] | None = None
    remarks: str | None = None


class UserUpdateByAdmin(UserBase):
    """
    Admin update schema - admins can update everything including email and user_role.
    Used when admin updates worker information.
    """
    pass


# Alias for backward compatibility - defaults to admin update (full permissions)
UserUpdate = UserUpdateByAdmin

class UserLogin(BaseModel):
    email: str
    password: str

class UserRead(UserBase):
    id: int
    admin_id: int | None = None
    business_id: int | None = None

    class Config:
        from_attributes = True

class UserCreateResponse(BaseModel):
    """Response when creating a user: user data + access token for immediate use."""
    user: UserRead
    access_token: str
    token_type: str = "Bearer"


class UserTokenResponse(BaseModel):
    id: int
    name: str | None = None
    business_name: str | None = None
    email: EmailStr | None = None
    admin_id: int | None = None

    user_role: UserRoleEnum
    last_login_at: datetime | None = None
    access_token: str
    token_type: str
    
class ForgotPassword(BaseModel):
    email: str