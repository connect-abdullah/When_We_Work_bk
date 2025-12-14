from sqlalchemy.orm import Session
from app.entities.admin.schema import AdminCreate, AdminRead
from app.entities.admin.model import Admin
from app.core.logging import get_logger


logger = get_logger(__name__)

class AdminService:
    def __init__(self, db : Session) -> None:
        self.db = db
        
    # Create admin
    def create_admin(self, payload: AdminCreate) -> AdminRead:
        try:
            admin = Admin(**payload.model_dump()) # dumping the payload as json so it can be read as it is
            self.db.add(admin) # add that admin payload into database
            self.db.commit() # making new changes/commiting new change to the database.
            self.db.refresh(admin) # Refresh the admin instance to get its up-to-date state from the database, as it is going to return whole payload with different fields as response
            return AdminRead.model_validate(admin)
        except Exception as e:
            logger.error(f"Error creating admin: {str(e)}")
            raise
    
    # Get admin by admin_id
    def get_admin_by_id(self, admin_id: int) -> AdminRead:
        try:
            admin = self.db.query(Admin).filter(Admin.id == admin_id).first()
            if (admin):
                return AdminRead.model_validate(admin)
            return None
        except Exception as e:
            logger.error(f"Error retrieving admin: {str(e)}")
            raise
        
    # Get all admins by business_id
    def get_all_admins(self, business_id: str) -> list[AdminRead]:
        try: 
            all_admins = self.db.query(Admin).filter(Admin.business_id == business_id).all()
            
            if not all_admins:
                return []
            
            return [AdminRead.model_validate(admin) for admin in all_admins]
        except Exception as e:
            logger.error(f"Error retrieving all admins: {str(e)}")
            raise

    # Update admin by admin_id
    def update_admin(self, admin_id:int , payload: AdminCreate) -> AdminRead:
        try:
            admin = self.db.query(Admin).filter(Admin.id == admin_id).first()
            
            if not admin:
                return None
            
            for key, value in payload.model_dump().items():
                setattr(admin, key, value)
            
            self.db.commit()
            self.db.refresh(admin)

            return AdminRead.model_validate(admin)
        
        except Exception as e:
            logger.error(f"Error updating admin: {str(e)}")
            raise
        
    # Delete admin by admin_id
    def delete_admin(self, admin_id:int) -> bool:
        try:
            admin = self.db.query(Admin).filter(Admin.id == admin_id).first()
            
            if not admin:
                return False
            
            self.db.delete(admin)
            self.db.commit()

            return True
        except Exception as e:
            logger.error(f"Error deleting admin: {str(e)}")
            raise

