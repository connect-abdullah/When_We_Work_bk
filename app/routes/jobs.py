from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.core.auth import get_current_admin_id
from app.entities.jobs.service import JobService
from app.entities.jobs.schema import JobCreate, JobRead, JobUpdate, JobStats
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

# Create Job (requires admin; admin_id from token, not from frontend)
@router.post("", response_model=APIResponse[JobRead])
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Create new job. Admin only; admin_id is set from token."""
    try:
        new_job = JobService(db).create_job(job, admin_id=admin_id)
        return ok(data=new_job, message="Job Created Successfully")
    except Exception as e:
        return fail(message=str(e))


# Get Job Stats (requires admin; uses admin_id from token)
@router.get("/stats", response_model=APIResponse[JobStats])
def get_job_stats(
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Get job stats for the logged-in admin."""
    try:
        job_stats = JobService(db).get_jobs_stats(admin_id)
        return ok(data=job_stats, message="Job Stats Found Successfully")
    except Exception as e:
        return fail(message=str(e))


# Get Job by Job ID (requires admin)
@router.get("/{job_id}", response_model=APIResponse[JobRead])
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Get job by job_id. Admin only."""
    try:
        job = JobService(db).get_job_by_id(job_id)
        return ok(data=job, message="Job Found Successfully")
    except Exception as e:
        return fail(message=str(e))


# Get All Jobs (requires admin; uses admin_id from token)
@router.get("", response_model=APIResponse[List[JobRead]])
def get_all_jobs(
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Get all jobs for the logged-in admin."""
    try:
        all_jobs = JobService(db).get_all_jobs(admin_id)
        return ok(data=all_jobs, message="Jobs Found Successfully")
    except Exception as e:
        return fail(message=str(e))


# Update Job by Job ID (requires admin)
@router.put("/{job_id}", response_model=APIResponse[JobRead])
def update_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Update job by job_id. Admin only."""
    try:
        updated_job = JobService(db).update_job(job_id, job)
        if not updated_job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return ok(data=updated_job, message="Job Updated Successfully")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))


# Delete Job by Job ID (requires admin)
@router.delete("/{job_id}", response_model=APIResponse[bool])
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Delete job by job_id. Admin only."""
    try:
        deleted = JobService(db).delete_job(job_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )
        return ok(data=True, message="Job Deleted Successfully")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))