from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.jobs.service import JobService
from app.entities.jobs.schema import JobCreate, JobRead, JobUpdate, JobStats

router = APIRouter(
    prefix = "/jobs",
    tags = ["Jobs"]
)

# Create Job
@router.post("", response_model=APIResponse[JobRead])
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """ Create new job """
    try:
        new_job = JobService(db).create_job(job)
        return ok(data=new_job, message="Job Created Successfully")
    except Exception as e:
        return fail(message=str(e))

# Get Job Stats by Admin ID (must be before /{job_id} so "stats" is not captured as job_id)
@router.get("/stats", response_model=APIResponse[JobStats])
def get_job_stats(admin_id: int, db: Session = Depends(get_db)):
    """ Get job stats by admin_id """
    try:
        job_stats = JobService(db).get_jobs_stats(admin_id)
        return ok(data=job_stats, message="Job Stats Found Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Get Job by Job ID
@router.get("/{job_id}", response_model=APIResponse[JobRead])
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    """ Get job by job_id """
    try:
        job = JobService(db).get_job_by_id(job_id)
        return ok(data=job, message="Job Found Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Get All Jobs by Admin ID
@router.get("", response_model=APIResponse[List[JobRead]])
def get_all_jobs(admin_id: int, db: Session = Depends(get_db)):
    """ Get all jobs by admin_id """
    try:
        all_jobs = JobService(db).get_all_jobs(admin_id)
        return ok(data=all_jobs, message="Jobs Found Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Update Job by Job ID  
@router.put("/{job_id}", response_model=APIResponse[JobRead])
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    """ Update job by job_id """
    try:
        updated_job = JobService(db).update_job(job_id, job)
        if not updated_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        return ok(data=updated_job, message="Job Updated Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Delete Job by Job ID
@router.delete("/{job_id}", response_model=APIResponse[dict])
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """ Delete job by job_id """
    try:
        deleted_job = JobService(db).delete_job(job_id)
        return ok(data=deleted_job, message="Job Deleted Successfully")
    except Exception as e:
        return fail(message=str(e))