from datetime import date, datetime
from pydantic import BaseModel
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
    pass

class AdminUpdate(AdminBase):
    pass
     
class AdminRead(AdminBase):
    id: int
    
    class Config:
        from_attributes = True

