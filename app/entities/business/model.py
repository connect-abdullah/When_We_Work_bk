from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base, BaseModel

class Business(Base, BaseModel):
    __tablename__ = "business"
    
    business_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    description = Column(String, nullable=False)
    