from app.routes.workers import router as workers_router
from app.routes.admin import router as admin_router
from app.routes.jobs import router as jobs_router
from app.routes.business import router as business_router

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(workers_router)
router.include_router(admin_router)
router.include_router(jobs_router)
router.include_router(business_router)