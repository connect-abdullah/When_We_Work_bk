from sqlalchemy.orm import Session
from app.entities.business.schema import BusinessCreate, BusinessRead, BusinessUpdate
from app.entities.business.model import Business
from app.core.logging import get_logger

logger = get_logger(__name__)

class BusinessService:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    # Create a business
    def create_business(self, payload: BusinessCreate) -> BusinessRead:
        try:
            business = Business(**payload.model_dump())
            self.db.add(business)
            self.db.commit()
            self.db.refresh()
            return BusinessRead.model_validate(business)
        except Exception as e:
            logger.error(f"Error creating a business: {str(e)}")
            
    # Get a business by business_id
    def get_business_by_id(self, business_id: int) -> BusinessRead:
        try:
            business = self.db.query(Business).filter(Business.id == business_id)
            if(business): 
                return BusinessRead.model_validate(business)
            return None
        except Exception as e:
            logger.error(f"Error getting a business: {str(e)}")

    # Get all businesses
    def get_all_businesses(self) -> list[BusinessRead]:
        try:
            all_businesses = self.db.query(Business)
            if(all_businesses): 
                return [BusinessRead.model_validate(business) for business in all_businesses]
            return []
        except Exception as e:
            logger.error(f"Error getting businesses: {str(e)}")
    
    # Update a business by business_id
    def update_business(self, business_id: int, payload: BusinessUpdate) -> BusinessRead:
        try:
            business = self.db.query(Business).filter(Business.id == business_id)
            if(business): 
                for key, value in payload.model_dump().items():
                    setattr(business, key, value)
                self.db.commit()
                self.db.refresh(business)
                return BusinessRead.model_validate(business)
            return None
        except Exception as e:
            logger.error(f"Error updating a business: {str(e)}")
    
    # Delete a business by business_id
    def delete_business(self, business_id: int) -> bool:
        try:
            business = self.db.query(Business).filter(Business.id == business_id)
            if(business): 
                self.db.delete(business)
                self.db.commit()
                self.db.refresh()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting a business: {str(e)}")