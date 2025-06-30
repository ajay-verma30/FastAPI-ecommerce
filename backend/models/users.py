from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from db.conn import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active  =Column(Boolean, default=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    pincode = Column(String(10), nullable=False)
    landmark = Column(String(100), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    phone = Column(String(20), nullable=True, unique=True, index=True)