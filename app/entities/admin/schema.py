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
    gender: Gender | None = None
    role: UserRoleEnum = UserRoleEnum.ADMIN
    business_id: int
    
    class Config:
        from_attributes = True
    
class AdminCreate(AdminBase):
    pass

class AdminUpdate(AdminBase):
    pass
     
class AdminRead(AdminBase):
    id: int
    
    class Config:
        from_attributes = True

