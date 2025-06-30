from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.conn import get_db
from models.admin import Admin
from schemas.admin import AdminCreate, AdminLogin, AdminOut
from utils.token import get_current_admin, create_access_token
from utils.auth import hash_password, verify_password

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/register", response_model=AdminOut)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(Admin).filter(or_(Admin.email == admin.email, Admin.username == admin.username)).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Admin with this email/username already exists. Try log in instead"
        )

    hashed_pwd = hash_password(admin.password)
    new_admin = Admin(
        username=admin.username,
        email=admin.email,
        password=hashed_pwd
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin



@router.post("/login")
def login(admin: AdminLogin, db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.username == admin.username).first()
    
    if not db_admin or not verify_password(admin.password, db_admin.password):  # FIXED HERE
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token(data={"sub": str(db_admin.id)})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }