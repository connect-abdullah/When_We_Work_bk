from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel


class JobApplicationStatus(str, Enum):
    applied = "applied"
    approved = "approved"
    rejected = "rejected"

class WorkStatus(str, Enum):
    pending = "pending"
    assigned = "assigned"
    completed = "completed"

class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    rejected = "rejected"

class JobApplication(Base, BaseModel):
    __tablename__ = "job_applications"
    __table_args__ = (UniqueConstraint('job_id', 'worker_id', name='uix_job_application_job_id_worker_id'),)
    
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_status = Column(SQLAEnum(JobApplicationStatus), nullable=False)
    work_status = Column(SQLAEnum(WorkStatus), nullable=True)
    payment_status = Column(SQLAEnum(PaymentStatus), nullable=True)
    # relationship for easy data access and retrieval
    job = relationship("Job", backref="job_applications")  # backref automatically creates job.job_applications
    user = relationship("User", backref="job_applications")  # backref automatically creates user.job_applications