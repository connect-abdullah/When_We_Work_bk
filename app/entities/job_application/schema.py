from pydantic import BaseModel, ConfigDict
from app.entities.job_application.model import JobApplicationStatus
from app.entities.user.schema import Gender, EmploymentType

class JobApplicationBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    job_id: int
    approved_status: JobApplicationStatus = JobApplicationStatus.applied
    
class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationRead(JobApplicationBase):
    id: int
    worker_id: int
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
class JobApplicationUpdate(JobApplicationBase):
    pass

class JobApproval(BaseModel):
    id: int
    job_id: int
    job_name: str
    worker_id: int
    worker_name: str
    worker_email: str
    availability: bool
    gender: Gender
    workers_required: int | None = None
    workers_hired: int | None = None
    employment_type: EmploymentType | None = None