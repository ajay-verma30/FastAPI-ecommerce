from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    user_id: int
    shipping_address: str
    total_amount: float
    order_items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    status: str
    total_amount: float
    shipping_address: str
    payment_status: str
    order_items: List[OrderItemOut]

    class Config:
        from_attributes = True
