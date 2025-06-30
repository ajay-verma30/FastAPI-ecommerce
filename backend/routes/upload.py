from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from db.conn import get_db
from models.items import Items, CategoryEnum, SubCategoryEnum, OrientationEnum
from models.admin import Admin 
import io

router = APIRouter(
    prefix="/import", 
    tags=["Excel Import"]
    )

@router.post("/items")
async def import_items_from_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")
    
    content = await file.read()
    df = pd.read_excel(io.BytesIO(content))

    items = []
    for _, row in df.iterrows():
        try:
            item = Items(
                product_name=row['product_name'],
                product_description=row['product_description'],
                product_category=CategoryEnum(row['product_category']),
                product_subcategory=SubCategoryEnum(row['product_subcategory']),
                orientation=OrientationEnum(row['orientation']),
                price=float(row['price']),
                quantity=int(row['quantity']),
                is_on_sale=bool(row['is_on_sale']),
                added_by=1 
            )
            items.append(item)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing row: {e}")
    
    db.bulk_save_objects(items)
    db.commit()

    return {"message": f"{len(items)} items imported successfully"}
