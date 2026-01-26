from app.entities.jobs.schema import JobRead
from sqlalchemy.orm import Session
from app.entities.job_application.schema import JobApplicationCreate, JobApplicationRead, JobApplicationUpdate
from app.entities.job_application.model import JobApplication
from app.core.logging import get_logger

logger = get_logger(__name__)

class JobApplicationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    # Create job application
    def create_job_application(self, payload: JobApplicationCreate) -> JobApplicationRead:
        try:
            job_application = JobApplication(**payload.model_dump())
            self.db.add(job_application)
            self.db.commit()
            self.db.refresh()
            return JobRead.model_validate(job_application)
        except Exception as e:
            logger.error(f"Error creating job application: {str(e)}")
            raise
    
    # Get job application by id
    def get_job_application_by_id(self, job_application_id: int) -> JobApplicationRead:
        try:
            job_application = self.db.query(JobApplication).filter(job_application.id == job_application_id)
            if(job_application):
                return JobApplicationRead.model_validate(job_application)
            return None
        except Exception as e:
            logger.error(f"Error getting a job application: {str(e)}")
    
    # Get all job applications
    def get_all_job_applications(self, worker_id:int) -> list[JobApplicationRead]:
        try:
            all_job_applications = self.db.query(JobApplication).filter(JobApplication.worker_id == worker_id)
            if(all_job_applications):
                return [JobApplicationRead.model_validate(job_application) for job_application in all_job_applications]
            return []
        except Exception as e:
            logger.error(f"Error getting all job applications: {str(e)}")
        
    # Delete job application
    def delete_job_application(self, job_id: int) -> JobApplicationRead:
        try:
            job_application = self.db.query(JobApplication).filter(JobApplication.job_id == job_id)
            if(job_application):
                self.db.delete(job_application)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting a job application: {str(e)}")
            
    # Update job application
    def update_job_application(self, job_application_id: int, payload: JobApplicationUpdate) -> JobApplicationRead:
        try:
            job_application = self.db.query(JobApplication).filter(JobApplication.id == job_application_id)
            if(job_application):
                for key, value in payload.model_dump().items():
                    setattr(job_application, key, value)
                self.db.commit()
                self.db.refresh(job_application)
                return JobRead.model_validate(job_application)
            return None
        except Exception as e:
            logger.error(f"Error updating a job application: {str(e)}")
        