from this import d
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.business.service import BusinessService
from app.entities.business.schema import BusinessCreate, BusinessRead, BusinessUpdate

router = APIRouter(
    prefix = "/business",
    tags = ["Business"]
)

# Create Business
@router.post("", response_model=APIResponse[BusinessRead])
def create_business(business: BusinessCreate, db: Session = Depends(get_db)):
    """ Create a business """
    try:
        new_business = BusinessService.create_business(business)
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
    
@router.get("", response_model=APIResponse[List[BusinessRead]])
def get_all_businesses(db:Session = Depends(get_db)):
    """ Get All Businesses """
    try:
        all_businesses = BusinessService(db).get_all_businesses()
        return ok(data=all_businesses, message="All Businesses Found Successfully")
    except Exception as e:
        return fail(message=str(e))
    
# Update Business
@router.put("/{business_id}", response_model=APIResponse[BusinessRead])
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
@router.delete("/{business_id}", response_model=APIResponse[dict])
def delete_business(business_id: int, db: Session = Depends(get_db)):
    """ Delete a business """
    try:
        deleted_business = BusinessService(db).delete_business(business_id=business_id)
        if not deleted_business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )
        return ok(data=deleted_business, message="Business Deleted Successfully")
    except Exception as e:
        return fail(message=str(e))