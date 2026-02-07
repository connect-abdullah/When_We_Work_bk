from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel


class JobApplicationStatus(str, Enum):
    applied = "applied"
    approved = "approved"
    rejected = "rejected"

class JobApplication(Base, BaseModel):
    __tablename__ = "job_applications"
    
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_status = Column(SQLAEnum(JobApplicationStatus), nullable=False)
    
    # relationship for easy data access and retrieval
    job = relationship("Job", backref="job_applications")  # backref automatically creates job.job_applications
    user = relationship("User", backref="job_applications")  # backref automatically creates user.job_applications