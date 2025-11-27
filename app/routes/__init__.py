from app.routes.staff import router as staff_router

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(staff_router)