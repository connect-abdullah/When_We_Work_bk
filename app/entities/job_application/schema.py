from pydantic import BaseModel, ConfigDict
from app.entities.job_application.model import JobApplicationStatus

class JobApplicationBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    job_id: int
    worker_id: int
    approved_status: JobApplicationStatus = JobApplicationStatus.pending
    
class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationRead(JobApplicationBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
class JobApplicationUpdate(JobApplicationBase):
    pass