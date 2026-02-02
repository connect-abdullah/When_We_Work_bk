from sqlalchemy.orm import Session
from app.entities.admin.schema import AdminCreate, AdminRead, AdminLogin, AdminTokenResponse
from app.entities.admin.model import Admin
from app.core.logging import get_logger
from app.core.security import verify_password, create_token, get_password_hash
from fastapi import HTTPException   
from time import time
from datetime import datetime, timezone

logger = get_logger(__name__)

class AdminService:
    def __init__(self, db : Session) -> None:
        self.db = db
        
    # Create admin
    def create_admin(self, payload: AdminCreate) -> AdminRead:
        try:
            if payload.password:
                payload.password = get_password_hash(payload.password) # hash the password
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
    def get_all_admins(self, business_id: int) -> list[AdminRead]:
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

    # Login admin
    def login_admin(self, payload: AdminLogin) -> AdminTokenResponse:
        try:
            admin = self.db.query(Admin).filter(Admin.email == payload.email).first()
            if not admin:
                raise HTTPException(status_code=401, detail="Admin not found")
            if not verify_password(payload.password, admin.password):
                raise HTTPException(status_code=401, detail="Invalid password")
            admin_data = {
                "id": admin.id,
                "name": f"{admin.first_name} {admin.last_name}",
                "business_name": admin.business.business_name,
                "email": admin.email,
                "role": admin.role.value if hasattr(admin.role, 'value') else str(admin.role),
                "last_login_at": datetime.now(timezone.utc)
            }
            token = create_token({"sub": str(admin.id), "role": admin.role.value if hasattr(admin.role, 'value') else str(admin.role)}) # 18000 seconds = 5 hours
            token_response = AdminTokenResponse(**admin_data , access_token=token, token_type="Bearer")
            return token_response
        except Exception as e:
            logger.error(f"Error logging in admin: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))