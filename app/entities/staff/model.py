from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Enum as SQLAEnum, Array
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel

class UserRoleEnum(str, Enum):
    ADMIN = "admin"         # System admin - can create jobs and appoint staff
    STAFF = "staff"         # Staff - can apply for jobs

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Staff(Base, BaseModel):
    __tablename__ = "staff"
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    
    language = Column(Array(String), nullable=False, default=["en"])
    gender = Column(SQLAEnum(Gender), nullable=False)
    
    role = Column(SQLAEnum(UserRoleEnum), default=UserRoleEnum.STAFF)
    provider = Column(String, nullable=False) # foriegn key of admin.id
    
    active_jobs = Column(Array(Integer), nullable=True)
    total_jobs = Column(Array(String), nullable=True)
    
    admin_id = Column(Integer, nullable=False)