from sqlalchemy import Column, String, Float, Boolean, DateTime,CHAR

from datetime import datetime
from database import Base

class ProductORM(Base):
    __tablename__ = "products"

    id          = Column(CHAR(36), primary_key=True, index=True)
    name        = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    price       = Column(Float, nullable=False)
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.now)
    updated_at  = Column(DateTime, default=datetime.now, onupdate=datetime.now)
