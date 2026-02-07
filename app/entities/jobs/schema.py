from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.entities.jobs.model import JobCategory, JobStatus, SalaryType

class JobBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    title: str
    description: str
    status: JobStatus
    minimum_education: str
    job_category: JobCategory
    characteristics: list[str] | None = None
    workers_required: int
    salary: int
    from_date_time: datetime
    to_date_time: datetime

class JobCreate(JobBase):
    salary_type: SalaryType = SalaryType.fixed
    pass

class JobUpdate(JobBase):
    pass

class JobRead(JobBase):
    id: int
    admin_id: int  # from backend only (set from token)
    workers_hired: int | None = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
class JobStats(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    workers_required: int
    workers_hired: int
    total_jobs: int
    active_jobs: int