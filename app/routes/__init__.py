from app.routes.jobs import router as jobs_router
from app.routes.business import router as business_router
from app.routes.job_applications import router as job_applications_router
from app.routes.user import router as user_router
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(jobs_router)
router.include_router(business_router)
router.include_router(job_applications_router)
router.include_router(user_router)