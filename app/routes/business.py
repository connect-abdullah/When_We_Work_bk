from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.business.service import BusinessService
from app.entities.business.schema import BusinessCreate, BusinessRead, BusinessUpdate, VerifyBusinessRegister

router = APIRouter(
    prefix="/business",
    tags=["Business"],
)

# Step 1: Submit business details → OTP sent to business email (business not created yet)
@router.post("/request-registration", response_model=APIResponse[dict])
def request_business_registration(business: BusinessCreate, db: Session = Depends(get_db)):
    """Submit business details. OTP is sent to the business email. Call verify-and-register with the OTP to complete registration."""
    try:
        BusinessService(db).request_registration(business)
        return ok(data={"message": "OTP sent to business email"}, message="OTP sent successfully")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))

# Step 2: Submit OTP → verify; only then create business
@router.post("/verify-and-register", response_model=APIResponse[BusinessRead])
def verify_and_register(payload: VerifyBusinessRegister, db: Session = Depends(get_db)):
    """Verify OTP and complete business registration. Business is created only if OTP is correct."""
    try:
        new_business = BusinessService(db).verify_and_register(payload.email, payload.otp)
        return ok(data=new_business, message="Business registered successfully")
    except HTTPException:
        raise
    except Exception as e:
        return fail(message=str(e))

# Direct create (no OTP) – e.g. for internal/admin use
@router.post("", response_model=APIResponse[BusinessRead])
def create_business(business: BusinessCreate, db: Session = Depends(get_db)):
    """Create a business directly without OTP (e.g. internal use). For normal flow use request-registration then verify-and-register."""
    try:
        new_business = BusinessService(db).create_business(business)
        return ok(data=new_business, message="Business Created Successfully!")
    except Exception as e:
        return fail(message=str(e))

# Get Business by ID
@router.get("/{business_id}", response_model=APIResponse[BusinessRead])
def get_business_by_id(business_id: int, db: Session = Depends(get_db)):
    """ Get Business by ID """
    try:
        business = BusinessService(db).get_business_by_id(business_id=business_id)
        return ok(data=business, message="Business Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Get All Businesses
@router.get("", response_model=APIResponse[List[BusinessRead]])
def get_all_businesses(db:Session = Depends(get_db)):
    """ Get All Businesses """
    try:
        all_businesses = BusinessService(db).get_all_businesses()
        return ok(data=all_businesses, message="All Businesses Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Update Business
@router.put("/{business_id}", response_model=APIResponse[BusinessUpdate])
def update_business(business_id: int, business: BusinessUpdate, db: Session = Depends(get_db)):
    """ Update a business """
    try:
        updated_business = BusinessService(db).update_business(business_id=business_id, payload=business)
        if not updated_business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )
        return ok(data=updated_business, message="Business Updated Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Delete Business
@router.delete("/{business_id}", response_model=APIResponse[bool])
def delete_business(business_id: int, db: Session = Depends(get_db)):
    """ Delete a business """
    try:
        deleted_business = BusinessService(db).delete_business(business_id=business_id)
        if not deleted_business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )
        return ok(data=True, message="Business Deleted Successfully")
    except Exception as e:
        return fail(message=str(e))