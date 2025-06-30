from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.conn import get_db
from models.orders import Order, OrderItem
from models.users import User
from models.items import Items
from schemas.orders import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_order = Order(
        user_id=order.user_id,
        shipping_address=order.shipping_address,
        total_amount=order.total_amount,
    )
    db.add(new_order)
    db.flush()  


    for item in order.order_items:
        db_item = db.query(Items).filter(Items.id == item.item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail=f"Item ID {item.item_id} not found")
        order_item = OrderItem(
            order_id=new_order.id,
            item_id=item.item_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/", response_model=list[OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
