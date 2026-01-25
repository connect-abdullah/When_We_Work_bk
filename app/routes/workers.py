from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.workers.service import WorkerService
from app.entities.workers.schema import WorkerCreate, WorkerRead, WorkerUpdate

router = APIRouter(
    prefix = "/workers",
    tags = ["Workers"]
)

# Create Worker
@router.post("", response_model=APIResponse[WorkerRead])
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    """ Create new worker """
    try:
        new_worker = WorkerService(db).create_worker(worker)
        return ok(data=new_worker, message="Worker Created Successfully")
    except Exception as e:
        return fail(message=str(e))

# Get all workers
@router.get("", response_model=APIResponse[List[WorkerRead]])
def get_workers(admin_id: int, db: Session = Depends(get_db)):
    """ Get all workers by admin_id """
    try:
        all_workers = WorkerService(db).get_all_workers(admin_id=admin_id)
        return ok(data=all_workers, message="Workers Found Successfully")
    except Exception as e:
        return fail(message=str(e))

# Get worker by id
@router.get("/{worker_id}", response_model=APIResponse[WorkerRead])
def get_worker_by_id(worker_id: int, db: Session = Depends(get_db)):
    """ Get worker by id """
    try:
        worker = WorkerService(db).get_worker_by_id(worker_id=worker_id)
        return ok(data=worker, message="Worker Found Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Update worker
@router.put("/{worker_id}",response_model=APIResponse[WorkerRead])
def update_worker(worker_id: int, worker: WorkerUpdate, db: Session = Depends(get_db)):
    """ Update worker by id """
    try:
        updated_worker = WorkerService(db).update_worker(worker_id=worker_id, payload=worker)
        if not updated_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )
        return ok(data=updated_worker, message="Worker Updated Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Delete Worker
@router.delete("/{worker_id}", response_model=APIResponse[dict])
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """ Delete worker by id """
    try:
        deleted_worker = WorkerService(db).delete_worker(worker_id=worker_id)
        if not deleted_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )
        return ok(data=deleted_worker, message="Worker Deleted Successfully")
    except Exception as e:
        return fail(message=str(e))