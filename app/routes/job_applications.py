from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.job_application.service import JobApplicationService
from app.entities.job_application.schema import JobApplicationCreate, JobApplicationRead, JobApplicationUpdate
from app.core.auth import get_current_worker_id

router = APIRouter(
    prefix = "/job_applications",
    tags = ["Job Applications"]
)

# Create Job Application
@router.post("", response_model=APIResponse[JobApplicationRead])
def create_job_application(job_application: JobApplicationCreate, db: Session = Depends(get_db), worker_id: int = Depends(get_current_worker_id)):
    """ Create a job application """
    try:
        new_job_application = JobApplicationService(db).create_job_application(job_application, worker_id=worker_id)
        return ok(data=new_job_application, message="Job Application Created Successfully!")
    except Exception as e:
        return fail(message=str(e))

# Get Job Application by ID
@router.get("/{job_application_id}", response_model=APIResponse[JobApplicationRead])
def get_job_application_by_id(job_application_id: int, db: Session = Depends(get_db)):
    """ Get Job Application by ID """
    try:
        job_application = JobApplicationService(db).get_job_application_by_id(job_application_id=job_application_id)
        return ok(data=job_application, message="Job Application Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get All Job Applications by Worker ID
@router.get("", response_model=APIResponse[List[JobApplicationRead]])
def get_all_job_applications(db:Session = Depends(get_db), worker_id: int = Depends(get_current_worker_id)):
    """ Get All Job Applications by Worker ID """
    try:
        all_job_applications = JobApplicationService(db).get_all_job_applications(worker_id=worker_id)
        return ok(data=all_job_applications, message="All Job Applications Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Update Job Application
@router.put("/{job_application_id}", response_model=APIResponse[JobApplicationRead])
def update_job_application(job_application_id: int, job_application: JobApplicationUpdate, db: Session = Depends(get_db)):
    """ Update a job application """
    try:
        updated_job_application = JobApplicationService(db).update_job_application(job_application_id=job_application_id, payload=job_application)
        if not updated_job_application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job Application not found"
            )
        return ok(data=updated_job_application, message="Job Application Updated Successfully")
    except Exception as e:
        return fail(message=str(e))
    
    # Delete Job Application
@router.delete("/{job_application_id}", response_model=APIResponse[dict])
def delete_job_application(job_application_id: int, db: Session = Depends(get_db)):
    """ Delete a job application """
    try:
        deleted_job_application = JobApplicationService(db).delete_job_application(job_application_id=job_application_id)
        if not deleted_job_application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job Application not found"
            )
        return ok(data=deleted_job_application, message="Job Application Deleted Successfully")
    except Exception as e:
        return fail(message=str(e))