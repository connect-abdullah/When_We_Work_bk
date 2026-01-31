from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.entities.jobs.model import JobCategory, JobStatus, ToneRequirement, SalaryType

class JobBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    title: str
    description: str
    status: JobStatus
    minimum_education: str
    job_category: JobCategory
    tone_requirement: ToneRequirement
    characteristics: list[str] | None = None
    workers_required: int
    workers_hired: int
    salary: int
    salary_type: SalaryType | None = None
    admin_id: int
    
class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class JobRead(JobBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
class JobStats(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    workers_required: int
    workers_hired: int
    total_jobs: int
    active_jobs: int