from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from db.conn import get_db
from models.items import Items
from schemas.items import ItemCreate, ItemOut
from utils.token import get_current_admin
from models.items import CategoryEnum, SubCategoryEnum, OrientationEnum

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.post("/add", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    new_item = Items(
        product_name=item.product_name,
        product_description=item.product_description,
        price=item.price,
        quantity=item.quantity,
        orientation=item.orientation,
        product_category=item.product_category,
        product_subcategory=item.product_subcategory,
        added_by = admin.id
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[ItemOut])
def get_items(
    db: Session = Depends(get_db),
    category: Optional[CategoryEnum] = Query(None),
    subcategory: Optional[SubCategoryEnum] = Query(None),
    orientation: Optional[OrientationEnum] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    is_on_sale: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    query = db.query(Items)

    if category:
        query = query.filter(Items.product_category == category)
    if subcategory:
        query = query.filter(Items.product_subcategory == subcategory)
    if orientation:
        query = query.filter(Items.orientation == orientation)
    if min_price is not None:
        query = query.filter(Items.price >= min_price)
    if max_price is not None:
        query = query.filter(Items.price <= max_price)
    if is_on_sale is not None:
        query = query.filter(Items.is_on_sale == is_on_sale)
    items = query.order_by(Items.created_at.desc()).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == item_id, Items.is_active == True).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item