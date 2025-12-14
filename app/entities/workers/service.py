from sqlalchemy.orm import Session
from app.entities.workers.schema import WorkerCreate, WorkerRead
from app.entities.workers.model import Worker
from app.core.logging import get_logger


logger = get_logger(__name__)

class WorkerService:
    def __init__(self, db : Session) -> None:
        self.db = db
        
    # Create worker
    def create_worker(self, payload: WorkerCreate) -> WorkerRead:
        try:
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