from pydantic import BaseModel
from typing import Optional, Literal

class ItemCreate(BaseModel):
    product_name: str
    product_description :str
    price: float
    quantity : int
    product_category: Literal[
        "shoes", "clothing", "accessories", "sportswear", "ethnic"
    ]
    product_subcategory: str
    orientation: Literal["male", "female", "boys", "girls"]
    added_by: int

class ItemOut(BaseModel):
    id: int
    product_name: str
    product_description: str
    price: float
    quantity: int
    is_on_sale: bool
    orientation: str
    product_category: str
    product_subcategory: str

    class Config:
        from_attributes = True
