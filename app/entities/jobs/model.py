from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel

class JobCategory(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCER = "freelancer"
    
class JobStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
class ToneRequirement(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FORMAL = "formal"
    FRIENDLY = "friendly"
    EMPATHIC = "empathetic"

class SalaryType(str, Enum):
    HOURLY = "hourly"
    FIXED = "fixed"
    
class Job(Base, BaseModel):
    __tablename__ = "jobs"
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLAEnum(JobStatus), nullable=False)
    
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    minimum_education = Column(String, nullable=False)
    job_category = Column(SQLAEnum(JobCategory), nullable=False)
    
    tone_requirement = Column(SQLAEnum(ToneRequirement), nullable=False)
    characteristics = Column(ARRAY(String), nullable=False)
    
    workers_required = Column(Integer, nullable=False) # number of workers required for the job
    workers_hired = Column(Integer, nullable=False) # number of workers hired for the job
    
    salary = Column(Integer, nullable=False)    
    salary_type = Column(SQLAEnum(SalaryType), nullable=False)
    language = Column(ARRAY(String), nullable=False)    # languages required for the job
    join_date = Column(DateTime, nullable=False) # date and time when the job will start
    
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False) # foreign key of admin.id

    # relationship for easy data access and retrieval
    admin = relationship("Admin")  # backref automatically creates admin.jobs