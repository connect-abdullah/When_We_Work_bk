from app.db.base import Base # re-export Base for model metadata discovery if needed

from app.entities.staff.model import Staff

__all__ = [
    "Base",
    "Staff"
]