from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.entities.jobs.schema import JobCreate, JobRead, JobStats, JobUpdate
from app.entities.jobs.model import Job, JobStatus
from app.core.logging import get_logger

logger = get_logger(__name__)

class JobService:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    # Create a job
    def create_job(self, payload: JobCreate) -> JobRead:
        try:
            job = Job(**payload.model_dump())
            self.db.add(job)
            self.db.commit()
            self.db.refresh(job)
            return JobRead.model_validate(job)
        except Exception as e:
            logger.error(f"Error creating job: {str(e)}")
            raise
        
    # Get a job by job_id
    def get_job_by_id(self, job_id: int) -> JobRead:
        try:
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if (job):
                return JobRead.model_validate(job)
            return None
        except Exception as e:
            logger.error(f"Error getting job by id: {str(e)}")
            raise
        
    # Get all jobs by admin_id
    def get_all_jobs(self, admin_id: int) -> list[JobRead]:
        try:
            all_jobs = self.db.query(Job).filter(Job.admin_id == admin_id).all()
            if (all_jobs):
                return [JobRead.model_validate(job) for job in all_jobs]
            return []
        except Exception as e:
            logger.error(f"Error getting all jobs: {str(e)}")
            raise
        
    # Update a job by job_id
    def update_job(self, job_id: int, payload: JobUpdate) -> JobRead:
        try:
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if (job):
                for key, value in payload.model_dump().items():
                    setattr(job, key, value)
                self.db.commit()
                self.db.refresh(job)
                return JobRead.model_validate(job)
            return None
        except Exception as e:
            logger.error(f"Error updating job: {str(e)}")
            raise
        
    # Delete a job by job_id
    def delete_job(self, job_id: int) -> bool:
        try:
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if (job):
                self.db.delete(job)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting job: {str(e)}")
            raise
        
    # Get job stats (totals of workers_required / workers_hired across all jobs for this admin)
    def get_jobs_stats(self, admin_id: int) -> JobStats:
        try:
            row = (
                self.db.query(
                    func.count(Job.id).label("total_jobs"),
                    func.coalesce(func.sum(Job.workers_required), 0).label("workers_required"),
                    func.coalesce(func.sum(Job.workers_hired), 0).label("workers_hired"),
                    func.sum(case((Job.status == JobStatus.active, 1), else_=0)).label("active_jobs"),
                )
                .filter(Job.admin_id == admin_id)
                .first()
            )
            total_jobs = row.total_jobs or 0
            workers_required = int(row.workers_required)
            workers_hired = int(row.workers_hired)
            active_jobs = int(row.active_jobs or 0)
            return JobStats(
                workers_required=workers_required,
                workers_hired=workers_hired,
                total_jobs=total_jobs,
                active_jobs=active_jobs,
            )
        except Exception as e:
            logger.error(f"Error getting job status: {str(e)}")
            raise