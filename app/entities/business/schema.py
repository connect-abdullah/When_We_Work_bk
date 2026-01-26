from pydantic import BaseModel, ConfigDict
from app.entities.business.model import Business

class BusinessBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    business_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    description: str

class BusinessCreate(BusinessBase):
    pass

class BusinessRead(BusinessBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
class BusinessUpdate(BusinessBase):
    pass
