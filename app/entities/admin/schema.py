from datetime import date, datetime
from pydantic import BaseModel, EmailStr
from app.entities.admin.model import UserRoleEnum, Gender

class AdminBase(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: str
    phone: str
    photo: str | None = None
    
    language: str = "en"
    gender: Gender
    role: UserRoleEnum = UserRoleEnum.admin
    
class AdminCreate(AdminBase):
    business_id: int | None = None
    password: str | None = None
    pass

class AdminUpdate(AdminBase):
    pass

class AdminLogin(BaseModel):
    email: str
    password: str

class AdminRead(AdminBase):
    id: int
    
    class Config:
        from_attributes = True

class AdminTokenResponse(BaseModel):
    id: int
    name: str | None = None
    business_name: str | None = None
    email: EmailStr | None = None

    role: UserRoleEnum
    last_login_at: datetime | None = None
    access_token: str
    token_type: str