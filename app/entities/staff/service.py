from sqlalchemy.orm import Session
from app.entities.staff.schema import StaffCreate, StaffRead
from app.entities.staff.model import Staff
from app.core.logging import get_logger


logger = get_logger(__name__)

class StaffServices:
    def __init__(self, db : Session) -> None:
        self.db = db
        
    def create_staff(self, payload: StaffCreate) -> StaffRead:
        try:
            staff = Staff(**payload.model_dump()) # dumping the payload as json so it can be read as it is
            self.db.add(staff) # add that staff payload into database
            self.db.commit() # making new changes/commiting new change to the database.
            self.db.refresh(staff) # Refresh the staff instance to get its up-to-date state from the database, as it is going to return whole payload with different fields as response
            return StaffRead.model_validate(staff)
        except Exception as e:
            logger.error(f"Error creating staff: {str(e)}")
            raise