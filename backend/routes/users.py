from fastapi import  APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.conn import get_db
from models.users import User
from schemas.users import UserCreate, UserOut, UserLogin,MyUserOut
from utils.token import get_current_admin, create_access_token, get_current_user
from utils.auth import hash_password, verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(or_(User.email == user.email, User.username == user.username)).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Admin with this email/username already exists. Try log in instead"
        )

    hashed_pwd = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        first_name = user.first_name,
        last_name= user.last_name,
        address = user.address,
        pincode=user.pincode,
        landmark = user.landmark,
        city=user.city,
        state = user.state,
        phone=user.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):  
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token(data={"sub": str(db_user.id)})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/all-users", response_model=list[UserOut])
def get_users(db:Session=Depends(get_db), admin=Depends(get_current_admin)):
    users=  db.query(User).all()
    return users

@router.get("/{id}", response_model=MyUserOut)
def get_my_user(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.id != id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    my_user = db.query(User).filter(User.id == id).first()
    
    if not my_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )


    return my_user