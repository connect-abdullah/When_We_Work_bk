from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.core.auth import get_current_admin_id
from app.entities.workers.service import WorkerService
from app.entities.workers.schema import WorkerCreate, WorkerRead, WorkerUpdate

router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
)

# Create Worker (requires admin; admin_id from token, not from frontend)
@router.post("", response_model=APIResponse[WorkerRead])
def create_worker(
    worker: WorkerCreate,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Create new worker. Admin only; admin_id is set from token."""
    try:
        new_worker = WorkerService(db).create_worker(worker, admin_id=admin_id)
        return ok(data=new_worker, message="Worker Created Successfully")
    except Exception as e:
        return fail(message=str(e))


# Get all workers (requires admin; admin_id from token)
@router.get("", response_model=APIResponse[List[WorkerRead]])
def get_workers(
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Get all workers for the logged-in admin."""
    try:
        all_workers = WorkerService(db).get_all_workers(admin_id=admin_id)
        return ok(data=all_workers, message="Workers Found Successfully")
    except Exception as e:
        return fail(message=str(e))


# Get worker by id (requires admin)
@router.get("/{worker_id}", response_model=APIResponse[WorkerRead])
def get_worker_by_id(
    worker_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Get worker by id. Admin only."""
    try:
        worker = WorkerService(db).get_worker_by_id(worker_id=worker_id)
        return ok(data=worker, message="Worker Found Successfully")
    except Exception as e:
        return fail(message=str(e))


# Update worker (requires admin)
@router.put("/{worker_id}", response_model=APIResponse[WorkerRead])
def update_worker(
    worker_id: int,
    worker: WorkerUpdate,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Update worker by id. Admin only."""
    try:
        updated_worker = WorkerService(db).update_worker(worker_id=worker_id, payload=worker)
        if not updated_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found",
            )
        return ok(data=updated_worker, message="Worker Updated Successfully")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))


# Delete Worker (requires admin)
@router.delete("/{worker_id}", response_model=APIResponse[bool])
def delete_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    admin_id: int = Depends(get_current_admin_id),
):
    """Delete worker by id. Admin only."""
    try:
        deleted_worker = WorkerService(db).delete_worker(worker_id=worker_id)
        if not deleted_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found",
            )
        return ok(data=True, message="Worker Deleted Successfully")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))