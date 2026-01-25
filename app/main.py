from fastapi import FastAPI
from app.config import settings
from app.routes import router

# Create FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
)

# Include the API router
app.include_router(router)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "WhenWeWork Backend API",
        "version": settings.version,
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}