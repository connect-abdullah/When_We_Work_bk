from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.entities.business.schema import BusinessCreate, BusinessRead, BusinessUpdate
from app.entities.business.model import Business
from app.core.logging import get_logger
from app.core.security import generate_random_otp
from app.core.email import EmailService
from app.core.pending_registration import set_pending, pop_pending

logger = get_logger(__name__)


class BusinessService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.email_service = EmailService()

    # Request registration: send OTP to business email, store pending. Do NOT create business yet.
    def request_registration(self, payload: BusinessCreate) -> None:
        email = payload.email.strip().lower()
        if self.db.query(Business).filter(Business.email == email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A business with this email is already registered.",
            )
        otp = generate_random_otp(6)
        self.email_service.send_email(
            payload.email,
            "Your OTP for WhenWeWork Business Registration",
            f"Your verification code is: {otp}. It expires in 10 minutes.",
        )
        set_pending(email, otp, payload.model_dump())

    # Verify OTP and only then create the business.
    def verify_and_register(self, email: str, otp: str) -> BusinessRead:
        key = email.strip().lower()
        entry = pop_pending(key)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP. Please request a new code.",
            )
        if entry["otp"] != otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect OTP.",
            )
        payload = BusinessCreate.model_validate(entry["payload"])
        if self.db.query(Business).filter(Business.email == key).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A business with this email is already registered.",
            )
        return self.create_business(payload)

    # Create a business (used after OTP verification or direct create)
    def create_business(self, payload: BusinessCreate) -> BusinessRead:
        try:
            business = Business(**payload.model_dump())
            self.db.add(business)
            self.db.commit()
            self.db.refresh(business)
            return BusinessRead.model_validate(business)
        except Exception as e:
            logger.error(f"Error creating a business: {str(e)}")
            
    # Get a business by business_id
    def get_business_by_id(self, business_id: int) -> BusinessRead:
        try:
            business = self.db.query(Business).filter(Business.id == business_id).first()
            if business: 
                return BusinessRead.model_validate(business)
            return None
        except Exception as e:
            logger.error(f"Error getting a business: {str(e)}")

    # Get all businesses
    def get_all_businesses(self) -> list[BusinessRead]:
        try:
            all_businesses = self.db.query(Business).all()
            if all_businesses: 
                return [BusinessRead.model_validate(business) for business in all_businesses]
            return []
        except Exception as e:
            logger.error(f"Error getting businesses: {str(e)}")
    
    # Update a business by business_id
    def update_business(self, business_id: int, payload: BusinessUpdate) -> BusinessRead:
        try:
            business = self.db.query(Business).filter(Business.id == business_id).first()
            if business: 
                for key, value in payload.model_dump().items():
                    setattr(business, key, value)
                self.db.commit()
                self.db.refresh(business)
                return BusinessRead.model_validate(business)
            return None
        except Exception as e:
            logger.error(f"Error updating a business: {str(e)}")
            raise
    
    # Delete a business by business_id
    def delete_business(self, business_id: int) -> bool:
        try:
            business = self.db.query(Business).filter(Business.id == business_id).first()
            if business: 
                self.db.delete(business)
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting a business: {str(e)}")