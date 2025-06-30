from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, Double, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.conn import Base
import enum

class OrientationEnum(enum.Enum):
    male = "male"
    female = "female"
    boys = "boys"
    girls = "girls"

class CategoryEnum(enum.Enum):
    shoes = "shoes"
    clothing = "clothing"
    accessories = "accessories"
    sportswear = "sportswear"
    ethnic = "ethnic"

class SubCategoryEnum(enum.Enum):
    sneakers = "sneakers"
    running_shoes = "running_shoes"
    formal_shoes = "formal_shoes"
    sandals = "sandals"
    boots = "boots"
    flip_flops = "flip_flops"
    t_shirts = "t_shirts"
    shirts = "shirts"
    jeans = "jeans"
    trousers = "trousers"
    hoodies = "hoodies"
    jackets = "jackets"
    shorts = "shorts"
    dresses = "dresses"
    skirts = "skirts"
    caps = "caps"
    belts = "belts"
    wallets = "wallets"
    watches = "watches"
    sunglasses = "sunglasses"
    bags = "bags"
    track_pants = "track_pants"
    gym_wear = "gym_wear"
    sports_shoes = "sports_shoes"
    sweatshirts = "sweatshirts"
    kurta = "kurta"
    saree = "saree"
    lehenga = "lehenga"
    sherwani = "sherwani"

class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    product_description = Column(Text, nullable=False)
    product_category = Column(Enum(CategoryEnum), nullable=False)
    product_subcategory = Column(Enum(SubCategoryEnum), nullable=False)
    orientation = Column(Enum(OrientationEnum), nullable=False)
    price = Column(Double, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    is_on_sale = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    added_by = Column(Integer, ForeignKey("admins.id"), nullable=False)
    admin = relationship("Admin", back_populates="items")