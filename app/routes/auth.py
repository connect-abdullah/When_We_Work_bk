from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.admin.service import AdminService

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

# Login
@router.post("/login/admin", response_model=APIResponse[str])
def login(email: str, password: str, db: Session = Depends(get_db)):
    """ Login """
    try:
        token = AdminService(db).login_admin(email, password)
        return ok(data=token, message="Login Successfully")
    except Exception as e:
        return fail(message=str(e))