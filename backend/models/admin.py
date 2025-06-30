from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime
from db.conn import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.items import Items
from datetime import datetime



class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_active  =Column(Boolean, default=True)
    items = relationship("Items", back_populates="admin")
    created_at = Column(DateTime, default=datetime.utcnow)