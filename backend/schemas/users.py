from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email:EmailStr
    password: str
    first_name : str
    last_name : str
    address : str
    pincode : str
    landmark : str
    city : str
    state : str
    phone : str

class UserOut(BaseModel):
    username: str
    email:EmailStr
    first_name : str
    last_name : str
    address : str
    pincode : str
    landmark : str
    city : str
    state : str
    phone : str
    class Config:
        from_attributes : True


class  UserLogin(BaseModel):
    username: str
    password: str