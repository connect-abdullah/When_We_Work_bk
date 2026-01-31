from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel

class UserRoleEnum(str, Enum):
    admin = "admin"         # System admin - can create jobs and appoint workers
    worker = "worker"         # Worker - can apply for jobs

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class EmploymentType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    freelancer = "freelancer"

class Worker(Base, BaseModel):
    __tablename__ = "workers"
    
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    
    emergency_contact = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    
    language = Column(ARRAY(String), nullable=True, default=["en"])
    gender = Column(SQLAEnum(Gender), nullable=False)
    availability = Column(Boolean, default=True)
    employment_type = Column(SQLAEnum(EmploymentType), nullable=False)
    
    user_role = Column(SQLAEnum(UserRoleEnum), default=UserRoleEnum.worker)
    roles = Column(ARRAY(String), nullable=False)
    remarks = Column(String, nullable=True)
    
    
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False) # foreign key of admin.id

    # relationship for easy data access and retrieval
    admin = relationship("Admin")  # backref automatically creates admin.workers