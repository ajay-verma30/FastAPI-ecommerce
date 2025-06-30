from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, Double, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.conn import Base

class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    product_description = Column(Text, nullable=False)
    price = Column(Double, nullable=False)
    is_on_sale = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    added_by = Column(Integer, ForeignKey("admins.id"), nullable=False)
    admin = relationship("Admin", back_populates="items")