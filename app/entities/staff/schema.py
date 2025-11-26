from datetime import date, datetime
from pydantic import BaseModel
from app.entities.staff.model import UserRoleEnum, Gender

class StaffBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    photo: str | None = None
    
    language: list[str]
    gender: Gender | None = None
    role: UserRoleEnum | None = None  
    provider: str
    
class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass
     
class StaffRead(StaffBase):
    id: int
    
    class Config:
        from_attributes = True