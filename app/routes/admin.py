from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.response import APIResponse, ok, fail
from app.entities.admin.service import AdminService
from app.entities.admin.schema import AdminCreate, AdminRead, AdminUpdate

router = APIRouter(
    prefix = "/admin",
    tags = ["Admin"]
)

# Create Admin
@router.post("", response_model=APIResponse[AdminRead])
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    """ Create new admin """
    try:
        
        new_admin = AdminService(db).create_admin(admin)
        return ok(data=new_admin, message="Admin Created Successfully")
    except Exception as e:
        return fail(message=str(e))

# Get all admins
@router.get("", response_model=APIResponse[List[AdminRead]])
def get_admins(business_id: int, db: Session = Depends(get_db)):
    """ Get all admins by business_id """
    try:
        all_admins = AdminService(db).get_all_admins(business_id=business_id)
        return ok(data=all_admins, message="Admins Found Successfully")
    except Exception as e:
        return fail(message=str(e))

# Get admin by id
@router.get("/{admin_id}", response_model=APIResponse[AdminRead])
def get_admin_by_id(admin_id: int, db: Session = Depends(get_db)):
    """ Get admin by id """
    try:
        admin = AdminService(db).get_admin_by_id(admin_id=admin_id)
        return ok(data=admin, message="Admin Found Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Update admin
@router.put("/{admin_id}",response_model=APIResponse[AdminRead])
def update_admin(admin_id: int, admin: AdminUpdate, db: Session = Depends(get_db)):
    """ Update admin by id """
    try:
        updated_admin = AdminService(db).update_admin(admin_id=admin_id, payload=admin)
        if not updated_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found"
            )
        return ok(data=updated_admin, message="Admin Updated Successfully")
    except Exception as e:
        return fail(message=str(e))
        
# Delete Admin
@router.delete("/{admin_id}", response_model=APIResponse[bool])
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    try:
        deleted_admin = AdminService(db).delete_admin(admin_id=admin_id)
        if not deleted_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin already deleted"
            )
        
        return ok(data=True, message="Admin Deleted Successfully")
    except Exception as e:
        return fail(message=str(e))

