from sqlalchemy.orm import Session
from app.entities.workers.schema import WorkerCreate, WorkerRead, WorkerTokenResponse, WorkerLogin
from app.entities.workers.model import Worker
from app.core.logging import get_logger
from app.core.email import EmailService
from app.core.security import get_password_hash, generate_random_password, verify_password, create_token
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from datetime import datetime, timezone

logger = get_logger(__name__)

class WorkerService:
    def __init__(self, db : Session) -> None:
        self.db = db
        self.email_service = EmailService()
# Pass the the email to send the email function
# Email function will generate password and send the email with the password 
# Password will be hashed and returned to the create_worker function to be saved in the database
# The create worker worker will take the password hash and save it in the database with the worker data
# It will return the worker data without the password telling that the user is created successfully

    # Send worker email with password
    def send_worker_email_with_password(self, email: str) -> str:
        try:
            random_password = generate_random_password(15)
            logger.info(f"Generated random password: {random_password}")
            password = get_password_hash(random_password)
            logger.info(f"Password hashed: {password}")
            self.email_service.send_email(email, "Your Password for WhenWeWork", "Your password is: " + random_password)
            logger.info(f"Password sent to email: {email}")
            return password
        except Exception as e:
            logger.error(f"Error sending worker email with password: {str(e)}")
            raise
        
    # Check if worker email already exists
    def check_worker_email_exists(self, email: str) -> bool:
        try:
            already_exists = self.db.query(Worker).filter(Worker.email == email).first()
            return already_exists is not None
        except Exception as e:
            logger.error(f"Error checking if worker email exists: {str(e)}")
            raise
    # Create worker
    def create_worker(self, payload: WorkerCreate) -> WorkerRead:
        try:
            already_exists = self.check_worker_email_exists(payload.email)
            if already_exists:
                logger.error(f"Worker with email {payload.email} already exists")
                raise ValueError("Worker with this email already exists")
            # Validate email format
            try:
                validate_email(payload.email)  # format only; skip MX check (allows example.com in dev)
            except EmailNotValidError as e:
                logger.error(f"Error validating email: {str(e)}")
                raise
            password = self.send_worker_email_with_password(payload.email)
            payload.password = password
            worker = Worker(**payload.model_dump()) # dumping the payload as json so it can be read as it is
            self.db.add(worker) # add that worker payload into database
            self.db.commit() # making new changes/commiting new change to the database.
            self.db.refresh(worker) # Refresh the worker instance to get its up-to-date state from the database, as it is going to return whole payload with different fields as response
            return WorkerRead.model_validate(worker)
        except Exception as e:
            logger.error(f"Error creating worker: {str(e)}")
            raise
    
    # Get worker by worker_id
    def get_worker_by_id(self, worker_id: int) -> WorkerRead:
        try:
            worker = self.db.query(Worker).filter(Worker.id == worker_id).first()
            if (worker):
                return WorkerRead.model_validate(worker)
            return None
        except Exception as e:
            logger.error(f"Error retrieving worker: {str(e)}")
            raise
        
    # Get all workers by admin_id
    def get_all_workers(self, admin_id: int) -> list[WorkerRead]:
        try: 
            all_workers = self.db.query(Worker).filter(Worker.admin_id == admin_id).all()
            
            if not all_workers:
                return []
            
            return [WorkerRead.model_validate(worker) for worker in all_workers]
        except Exception as e:
            logger.error(f"Error retrieving all workers: {str(e)}")
            raise
            
    # Update worker by worker_id
    def update_worker(self, worker_id:int , payload: WorkerCreate) -> WorkerRead:
        try:
            worker = self.db.query(Worker).filter(Worker.id == worker_id).first()
            
            if not worker:
                return None
            
            for key, value in payload.model_dump().items():
                setattr(worker, key, value)
            
            self.db.commit()
            self.db.refresh(worker)

            return WorkerRead.model_validate(worker)
        
        except Exception as e:
            logger.error(f"Error updating worker: {str(e)}")
            raise
        
    # Delete worker by worker_id
    def delete_worker(self, worker_id:int) -> bool:
        try:
            worker = self.db.query(Worker).filter(Worker.id == worker_id).first()
            
            if not worker:
                return False
            
            self.db.delete(worker)
            self.db.commit()

            return True
        except Exception as e:
            logger.error(f"Error deleting worker: {str(e)}")
            raise
        
    # Login worker
    def login_worker(self, payload: WorkerLogin) -> WorkerTokenResponse:
        try:
            worker = self.db.query(Worker).filter(Worker.email == payload.email).first()
            if not worker:
                raise HTTPException(status_code=401, detail="Worker not found")
            if not verify_password(payload.password, worker.password):
                raise HTTPException(status_code=401, detail="Invalid password")
            worker_data = {
                "id": worker.id,
                "name": f"{worker.first_name} {worker.last_name}",
                "email": worker.email,
                "role": worker.role.value if hasattr(worker.role, 'value') else str(worker.role),
                "last_login_at": datetime.now(timezone.utc)
            }
            token = create_token({"sub": str(worker.id), "role": worker.role.value if hasattr(worker.role, 'value') else str(worker.role)})
            token_response = WorkerTokenResponse(**worker_data , access_token=token, token_type="Bearer")
            return token_response
        except Exception as e:
            logger.error(f"Error logging in worker: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))