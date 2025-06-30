from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.conn import get_db
from models.items import Items
from schemas.items import ItemCreate, ItemOut
from utils.token import get_current_admin

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
def get_items(db: Session = Depends(get_db)):
    return db.query(Items)

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Items).filter(Items.id == item_id, Items.is_active == True).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item