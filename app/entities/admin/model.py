from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Enum as SQLAEnum
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel

class UserRoleEnum(str, Enum):
    ADMIN = "admin"         # System admin - can create jobs and appoint staff
    STAFF = "staff"         # Staff - can apply for jobs

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Admin(Base, BaseModel):
    __tablename__ = "admin"
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    
    language = Column(String, nullable=False, default="en")
    gender = Column(SQLAEnum(Gender), nullable=False)
    
    role = Column(SQLAEnum(UserRoleEnum), default=UserRoleEnum.ADMIN)
    business_id = Column(String, nullable=False) # foreign key of business.id (associated business)
    
    