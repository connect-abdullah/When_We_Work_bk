from sqlalchemy.orm import Session
from app.entities.staff.schema import StaffCreate, StaffRead
from app.entities.staff.model import Staff
from app.core.logging import get_logger


logger = get_logger(__name__)

class StaffService:
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
    
    def get_staff_by_id(self, staff_id: int) -> StaffRead:
        try:
            staff = self.db.query(Staff).filter(staff_id == id).first()
            if (staff):
                return StaffRead.model_validate(staff)
            return None
        except Exception as e:
            logger.error(f"Error retrieving staff: {str(e)}")
            raise
        
    def get_all_staff(self, admin_id: int) -> StaffRead:
        try: 
            all_staff = self.db.query(Staff).filter(Staff.admin_id == admin_id)
            
            if not all_staff:
                return None
            
            return [StaffRead.model_validate(staff) for staff in all_staff]
        except Exception as e:
                        logger.error(f"Error retrieving all staff: {str(e)}")

            
    def update_staff(self, staff_id:int , payload: StaffCreate) -> StaffRead:
        try:
            staff = self.db.query(Staff).filter(Staff.id == staff_id)
            
            if not staff:
                return None
            
            for key, value in payload.model_dump().items():
                setattr(staff, key, value)
            
            self.db.commit()
            self.db.refresh(staff)

            return StaffRead.model_validate(staff)
        
        except Exception as e:
            logger.error(f"Error updating staff: {str(e)}")
            raise
        
    def delete_staff(self, staff_id:int) -> bool:
        try:
            staff = self.db.query(Staff).filter(Staff.id == staff_id)
            
            if not staff:
                return False
            
            self.db.delete(staff)
            self.db.commit()
            self.db.refresh(staff)

            return True
        except Exception as e:
            logger.error(f"Error updating staff: {str(e)}")
            raise