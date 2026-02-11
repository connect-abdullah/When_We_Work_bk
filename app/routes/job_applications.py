from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.job_application.service import JobApplicationService, JobApplicationApprovalService
from app.entities.job_application.schema import JobApplicationCreate, JobApplicationRead, JobApplicationUpdate, JobApproval, JobApplicationWorkerStatus, WorkerRevenue, PaymentUpdate, AdminRevenue
from app.core.auth import get_current_worker_id, get_current_admin_id

router = APIRouter(
    prefix = "/job_applications",
    tags = ["Job Applications"]
)

# Create Job Application --- WORKER PANEL ---
@router.post("", response_model=APIResponse[JobApplicationRead])
def create_job_application(job_application: JobApplicationCreate, db: Session = Depends(get_db), worker_id: int = Depends(get_current_worker_id)):
    """ Create a job application """
    try:
        new_job_application = JobApplicationService(db).create_job_application(job_application, worker_id=worker_id)
        return ok(data=new_job_application, message="Job Application Created Successfully!")
    except Exception as e:
        return fail(message=str(e))

# Get All Job Applications by Admin ID --- ADMIN PANEL ---
@router.get("/approval-panel", response_model=APIResponse[List[JobApproval]])
def get_all_job_applications_by_admin(db: Session = Depends(get_db), admin_id: int = Depends(get_current_admin_id)):
    """ Get All Job Applications by Admin ID """
    try:
        all_job_applications = JobApplicationApprovalService(db).get_all_job_applications(admin_id=admin_id)
        return ok(data=all_job_applications, message="All Job Applications Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Approve Job Application --- ADMIN PANEL ---
@router.put("/approval-panel", response_model=APIResponse[JobApplicationUpdate])
def approve_job_application(job_application: JobApplicationRead, db: Session = Depends(get_db), admin_id: int = Depends(get_current_admin_id)):
    """ Approve a job application """
    try:
        approved_job_application = JobApplicationApprovalService(db).approve_job_application(payload=job_application)
        return ok(data=approved_job_application, message="Job Application Approved Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get All Job Applications by Worker ID --- WORKER PANEL ---
@router.get("/job-application-status-panel", response_model=APIResponse[List[JobApplicationWorkerStatus]])
def get_all_job_applications_by_worker(db: Session = Depends(get_db), worker_id: int = Depends(get_current_worker_id)):
    """ Get All Job Applications by Worker ID """
    try:
        all_job_applications = JobApplicationApprovalService(db).get_job_applications_by_worker_id(worker_id=worker_id)
        return ok(data=all_job_applications, message="All Job Applications Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get Job Application by ID --- WORKER PANEL ---
@router.get("/{job_application_id}", response_model=APIResponse[JobApplicationRead])
def get_job_application_by_id(job_application_id: int, db: Session = Depends(get_db)):
    """ Get Job Application by ID """
    try:
        job_application = JobApplicationService(db).get_job_application_by_id(job_application_id=job_application_id)
        return ok(data=job_application, message="Job Application Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get All Job Applications by Worker ID --- WORKER PANEL ---
@router.get("", response_model=APIResponse[List[JobApplicationRead]])
def get_all_job_applications(db:Session = Depends(get_db), worker_id: int = Depends(get_current_worker_id)):
    """ Get All Job Applications by Worker ID """
    try:
        all_job_applications = JobApplicationService(db).get_all_job_applications(worker_id=worker_id)
        return ok(data=all_job_applications, message="All Job Applications Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get Worker Revenue --- WORKER PANEL ---
@router.get("/worker/revenue", response_model=APIResponse[List[WorkerRevenue]])
def get_worker_revenue(
    db: Session = Depends(get_db),
    worker_id: int = Depends(get_current_worker_id),
):
    """Get worker revenue."""
    try:
        revenue = JobApplicationService(db).get_worker_revenue(worker_id)
        return ok(data=revenue, message="Worker Revenue Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get Pending Payment (Admin Revenue) --- ADMIN PANEL ---
@router.get("/admin/revenue", response_model=APIResponse[AdminRevenue])
def get_pending_payment(
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Get admin's pending payment revenue with list of workers awaiting payment."""
    try:
        revenue = JobApplicationService(db).get_pending_payment(admin_id)
        return ok(data=revenue, message="Pending Payment Found Successfully")
    except Exception as e:
        return fail(message=str(e))

# @router.update("/admin/revenue", response_model=APIResponse[List[AdminRevenue]])
# def update_payment_status(
#     payload: PaymentUpdate,
#     db: Session = Depends(get_db),
#     admin_id: int = Depends(get_current_admin_id),
# ):
#     """Update payment status."""
#     try:
#         revenue = JobApplicationService(db).update_payment_status(admin_id, payload)
#         return ok(data=revenue, message="Payment Status Updated Successfully")
#     except Exception as e:
#         return fail(message=str(e))
    
# Update Job Application --- WORKER PANEL ---
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
    
    # Delete Job Application --- WORKER PANEL ---
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
    
