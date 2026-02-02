from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.admin.service import AdminService
from app.entities.admin.schema import AdminLogin, AdminTokenResponse
from app.entities.workers.service import WorkerService
from app.entities.workers.schema import WorkerLogin, WorkerTokenResponse

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

# Login Admin
@router.post("/login/admin", response_model=APIResponse[AdminTokenResponse])
def login(payload: AdminLogin, db: Session = Depends(get_db)):
    """ Login Admin """
    try:
        token = AdminService(db).login_admin(payload)
        return ok(data=token, message="Login Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Login Worker
@router.post("/login/worker", response_model=APIResponse[WorkerTokenResponse])
def login_worker(payload: WorkerLogin, db: Session = Depends(get_db)):
    """ Login Worker """
    try:
        token = WorkerService(db).login_worker(payload)
        return ok(data=token, message="Login Successfully")
    except Exception as e:
        return fail(message=str(e))