from sqlalchemy.orm import Session, joinedload
from app.entities.job_application.schema import JobApplicationCreate, JobApplicationRead, JobApplicationUpdate, JobApproval, JobApplicationWorkerStatus, WorkerRevenue, Revenue, AdminRevenue, PendingRevenue
from app.entities.job_application.model import JobApplication, JobApplicationStatus, WorkStatus, PaymentStatus
from app.entities.jobs.model import Job
from app.core.logging import get_logger

logger = get_logger(__name__)

class JobApplicationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    # Create job application
    def create_job_application(self, payload: JobApplicationCreate, worker_id: int) -> JobApplicationRead:
        try:
            data = payload.model_dump() | {"worker_id": worker_id}
            job_application = JobApplication(**data)
            self.db.add(job_application)
            self.db.commit()
            self.db.refresh(job_application)
            return JobApplicationRead.model_validate(job_application)
        except Exception as e:
            logger.error(f"Error creating job application: {str(e)}")
            raise
    
    # Get job application by id
    def get_job_application_by_id(self, job_application_id: int) -> JobApplicationRead:
        try:
            job_application = self.db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
            if job_application:
                return JobApplicationRead.model_validate(job_application)
            return None
        except Exception as e:
            logger.error(f"Error getting a job application: {str(e)}")
    
    # Get all job applications
    def get_all_job_applications(self, worker_id:int) -> list[JobApplicationRead]:
        try:
            all_job_applications = self.db.query(JobApplication).filter(JobApplication.worker_id == worker_id).all()
            if all_job_applications:
                return [JobApplicationRead.model_validate(job_application) for job_application in all_job_applications]
            return []
        except Exception as e:
            logger.error(f"Error getting all job applications: {str(e)}")
        
    # Delete job application
    def delete_job_application(self, job_id: int) -> bool:
        try:
            job_application = self.db.query(JobApplication).filter(JobApplication.job_id == job_id).first()
            if job_application:
                self.db.delete(job_application)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting a job application: {str(e)}")
            
    # Update job application
    def update_job_application(self, job_application_id: int, payload: JobApplicationUpdate) -> JobApplicationRead:
        try:
            job_application = self.db.query(JobApplication).filter(JobApplication.id == job_application_id).first()
            if job_application:
                for key, value in payload.model_dump().items():
                    setattr(job_application, key, value)
                self.db.commit()
                self.db.refresh(job_application)
                return JobApplicationRead.model_validate(job_application)
            return None
        except Exception as e:
            logger.error(f"Error updating a job application: {str(e)}")
            
    def get_worker_revenue(self, worker_id: int) -> list[WorkerRevenue]:
        try:
            job_applications = (
                self.db.query(JobApplication)
                .filter(
                    JobApplication.worker_id == worker_id,
                    JobApplication.work_status == WorkStatus.completed
                )
                .all()
            )
            return [
                WorkerRevenue(
                    total_salary=sum(ja.job.salary for ja in job_applications),
                    jobs=[
                        Revenue(
                            job_id=ja.job_id,
                            job_name=ja.job.title,
                            salary=ja.job.salary,
                            from_date_time=ja.job.from_date_time,
                            to_date_time=ja.job.to_date_time
                        )
                        for ja in job_applications
                    ]
                )
                for ja in job_applications
            ]
        except Exception as e:
            logger.error(f"Error getting worker revenue: {str(e)}")
            raise
        
    def get_pending_payment(self, admin_id: int) -> AdminRevenue:
        try:
            # Use join to filter by admin_id through the Job relationship
            job_applications = (
                self.db.query(JobApplication)
                .join(Job, JobApplication.job_id == Job.id)
                .filter(
                    Job.admin_id == admin_id,
                    JobApplication.payment_status == PaymentStatus.pending
                )
                .options(joinedload(JobApplication.job), joinedload(JobApplication.user))
                .all()
            )
            
            # Calculate total pending payment
            pending_payment = sum(ja.job.salary for ja in job_applications)
            
            # Build list of pending revenue items
            jobs = [
                PendingRevenue(
                    job_id=ja.job_id,
                    job_name=ja.job.title,
                    salary=ja.job.salary,
                    from_date_time=ja.job.from_date_time,
                    to_date_time=ja.job.to_date_time,
                    worker_id=ja.worker_id,
                    worker_name=f"{ja.user.first_name} {ja.user.last_name}",
                    worker_email=ja.user.email,
                    payment_status=ja.payment_status
                )
                for ja in job_applications
            ]
            
            return AdminRevenue(
                pending_payment=pending_payment,
                jobs=jobs
            )
        except Exception as e:
            logger.error(f"Error getting pending payment: {str(e)}")
            raise

# Approve Job application approval by admin
class JobApplicationApprovalService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def approve_job_application(self, payload: JobApplicationRead) -> JobApplicationUpdate:
        try:
            job_application = self.db.query(JobApplication).filter(JobApplication.id == payload.id and JobApplication.worker_id == payload.worker_id).first()
            if job_application:
                job_application.approved_status = payload.approved_status
                job_application.work_status = WorkStatus.assigned
                # Initialize workers_hired to 0 if it's None
                if job_application.job.workers_hired is None:
                    job_application.job.workers_hired = 0
                job_application.job.workers_hired += 1
                self.db.commit()
                self.db.refresh(job_application)
                return JobApplicationUpdate.model_validate(job_application)
            return None
        except Exception as e:
            logger.error(f"Error approving a job application: {str(e)}")
            
    def get_all_job_applications(self, admin_id: int) -> list[JobApproval]:
        try:
            rows = (
                self.db.query(JobApplication)
                .options(joinedload(JobApplication.job), joinedload(JobApplication.user))
                .filter(JobApplication.user.has(admin_id=admin_id), JobApplication.approved_status == JobApplicationStatus.applied)
                .all()
            )
            return [
                JobApproval(
                    id=ja.id,
                    job_id=ja.job_id,
                    job_name=ja.job.title,
                    worker_id=ja.worker_id,
                    worker_name=f"{ja.user.first_name} {ja.user.last_name}".strip(),
                    worker_email=ja.user.email,
                    availability=ja.user.availability or False,
                    gender=ja.user.gender,
                    employment_type=ja.user.employment_type,
                    workers_required=ja.job.workers_required,
                    workers_hired=ja.job.workers_hired,
                )
                for ja in rows
            ]
        except Exception as e:
            logger.error(f"Error getting all job applications: {str(e)}")
            raise
        
    def get_job_applications_by_worker_id(self, worker_id: int) -> list[JobApplicationWorkerStatus]:
        try:
            rows = self.db.query(JobApplication).options(joinedload(JobApplication.job)).filter(JobApplication.worker_id == worker_id).all()
            return [JobApplicationWorkerStatus(
                approved_status=ja.approved_status,
                job_details=ja.job
            ) for ja in rows]
        except Exception as e:
            logger.error(f"Error getting job applications by worker id: {str(e)}")
            raise