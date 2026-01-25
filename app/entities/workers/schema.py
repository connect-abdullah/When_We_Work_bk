from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.entities.workers.model import UserRoleEnum, Gender, EmploymentType

class WorkerBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: str
    phone: str
    
    address: str | None = None
    emergency_contact: str | None = None
    photo: str | None = None
    availability: bool = True
    language: list[str] | None = None
    gender: Gender
    employment_type: EmploymentType
    user_role: UserRoleEnum
    roles: list[str] | None = None
    remarks: str | None = None
    
class WorkerCreate(WorkerBase):
    pass

class WorkerUpdate(WorkerBase):
    pass
     
class WorkerRead(WorkerBase):
    id: int
    admin_id: int
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)