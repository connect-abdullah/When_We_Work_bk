from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.entities.job_application.model import JobApplicationStatus, WorkStatus
from app.entities.user.schema import Gender, EmploymentType
from app.entities.jobs.schema import JobBase, JobRead

class JobApplicationBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    job_id: int
    approved_status: JobApplicationStatus = JobApplicationStatus.applied
    work_status: WorkStatus = WorkStatus.pending
    
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
    
class JobApplicationWorkerStatus(BaseModel):
    approved_status: JobApplicationStatus
    job_details: JobRead
    model_config = ConfigDict(use_enum_values=True)
    
class Revenue(BaseModel):
    job_id: int
    job_name: str
    salary: float
    from_date_time: datetime | None = None
    to_date_time: datetime | None = None
    model_config = ConfigDict(use_enum_values=True) 
    
class WorkerRevenue(BaseModel):
    total_salary: float
    jobs: list[Revenue]
    model_config = ConfigDict(use_enum_values=True) 