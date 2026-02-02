from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base, BaseModel

class JobCategory(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    freelancer = "freelancer"
    
class JobStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    completed = "completed"
    cancelled = "cancelled"
    
class ToneRequirement(str, Enum):
    professional = "professional"
    casual = "casual"
    formal = "formal"
    friendly = "friendly"
    empathic = "empathetic"

class SalaryType(str, Enum):
    hourly = "hourly"
    fixed = "fixed"
    
class Job(Base, BaseModel):
    __tablename__ = "jobs"
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLAEnum(JobStatus), nullable=False)
    
    minimum_education = Column(String, nullable=False)
    job_category = Column(SQLAEnum(JobCategory), nullable=False)
    
    characteristics = Column(ARRAY(String), nullable=True)
    
    workers_required = Column(Integer, nullable=False) # number of workers required for the job
    workers_hired = Column(Integer, nullable=True) # number of workers hired for the job
    
    salary = Column(Integer, nullable=False)    
    salary_type = Column(SQLAEnum(SalaryType), nullable=False)
    from_date_time = Column(DateTime(timezone=True), nullable=False)    
    to_date_time = Column(DateTime(timezone=True), nullable=False)
    
    
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False) # foreign key of admin.id

    # relationship for easy data access and retrieval
    admin = relationship("Admin")  # backref automatically creates admin.jobs
    