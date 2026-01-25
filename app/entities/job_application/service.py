from sqlalchemy.orm import Session
from app.entities.jobs.schema import JobCreate, JobRead
from app.entities.jobs.model import Job
from app.core.logging import get_logger

logger = get_logger(__name__)

