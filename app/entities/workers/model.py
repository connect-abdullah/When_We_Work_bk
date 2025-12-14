from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, Array, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel

class UserRoleEnum(str, Enum):
    ADMIN = "admin"         # System admin - can create jobs and appoint workers
    WORKER = "worker"         # Worker - can apply for jobs

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCER = "freelancer"

class Worker(Base, BaseModel):
    __tablename__ = "workers"
    
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    
    emergency_contact = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    
    language = Column(Array(String), nullable=True, default=["en"])
    gender = Column(SQLAEnum(Gender), nullable=False)
    availability = Column(Boolean, default=True)
    employment_type = Column(SQLAEnum(EmploymentType), nullable=False)
    
    user_role = Column(SQLAEnum(UserRoleEnum), default=UserRoleEnum.WORKER)
    roles = Column(Array(String), nullable=False)
    remarks = Column(String, nullable=True)
    
    
    admin_id = Column(Integer, nullable=False) # foriegn key of admin.id