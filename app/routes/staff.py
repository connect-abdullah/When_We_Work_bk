from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.staff.service import StaffService
from app.entities.staff.schema import StaffCreate, StaffRead, StaffUpdate

router = APIRouter(
    prefix = "/staff",
    tags = ["Staff"]
)

# Create Staff
@router.post("", response_model=APIResponse[StaffRead])
def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    """ Create new staff """
    try:
        new_staff = StaffService(db).create_staff(staff)
        return ok(data=new_staff, message="Staff Member Created Successfully")
    except Exception as e:
        fail(message=str(e))

# Get all staff
@router.get("", response_model=APIResponse[StaffRead])
def get_staff(admin_id: int, db: Session = Depends(get_db)):
    """ Get all staff by admin_id """
    try:
        all_staff = StaffService(db).get_all_staff(admin_id=admin_id)
        return ok(data=all_staff, message="Staff Member Found Successfully")
    except Exception as e:
        fail(message=str(e))

# Get staff by id
@router.get("/{staff_id}", response_model=APIResponse[StaffRead])
def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    """ Get staff member by id """
    try:
        staff = StaffService(db).get_staff_by_id(staff_id=staff_id)
        return ok(data=staff, message="All Staff Found Successfully")
    except Exception as e:
        fail(message=str(e))
        
# Update staff
@router.put("/{staff_id}",response_model=APIResponse[StaffRead])
def update_staff(staff_id: int, db: Session = Depends(get_db)):
    """ Get staff member by id """
    try:
        updated_staff = StaffService(db).update_staff(staff_id=staff_id)
        if not updated_staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        return ok(data=updated_staff, message="Staff Member Updated Successfully")
    except Exception as e:
        fail(message=str(e))
        
# Delete Staff
@router.delete("/{staff_id}", response_model=APIResponse[dict])
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    try:
        staff = StaffService(db).delete_staff(staff_id=staff_id)
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member already deleted"
            )
        
        return ok(data=staff, message="Staff Member Deleted Succesfully")
    except Exception as e:
        fail(message=str(e))