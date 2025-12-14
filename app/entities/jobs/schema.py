from datetime import date, datetime
from pydantic import BaseModel
from app.entities.jobs.model import JobCategory, JobStatus, ToneRequirement, SalaryType

class JobBase(BaseModel):
    title: str
    description: str
    status: JobStatus
    email: str
    phone: str
    minimum_education: str
    job_category: JobCategory
    tone_requirement: ToneRequirement
    characteristics: list[str] | None = None
    workers_required: int
    workers_hired: int
    salary: int
    salary_type: SalaryType | None = None
    language: list[str] | None = None
    join_date: datetime | None = None
    
class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class JobRead(JobBase):
    id: int
    admin_id: int
    
    class Config:
        from_attributes = True