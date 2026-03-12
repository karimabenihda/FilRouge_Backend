from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.Furniture import Furniture, Category, SubCategory
from typing import List
from app.schemas.Furniture import (
    FurnitureInDB, FurnitureUpdate, FurnitureOut,
    CategoryInDB, CategoryOut, SubCategoryInDB, SubCategoryOut
)
from app.api.auth import get_current_user


furnitures_router = APIRouter()

# --- Furniture Endpoints ---
@furnitures_router.get("/furnitures", response_model=List[FurnitureOut])
def get_furnitures(db: Session = Depends(get_db)):
    return db.query(Furniture).all()


@furnitures_router.post("/furnitures", response_model=FurnitureOut)
def add_furniture(furniture: FurnitureInDB, db: Session = Depends(get_db),user=Depends(get_current_user)):
    new_furniture = Furniture(
        ProductName=furniture.ProductName,
        description=furniture.description,
        image=furniture.image,
        # brand=furniture.brand,
        price=furniture.price,
        stock=furniture.stock,
        subcategory_id=furniture.subcategory_id,
        created_at=datetime.utcnow()
    )
    db.add(new_furniture)
    db.commit()
    db.refresh(new_furniture)
    return new_furniture


@furnitures_router.put("/furnitures/{furniture_id}", response_model=FurnitureOut)
def update_furniture(furniture_id: int, new_data: FurnitureUpdate, db: Session = Depends(get_db),user=Depends(get_current_user)):
    furniture = db.query(Furniture).filter(Furniture.ProductID == furniture_id).first()
    if not furniture:
        raise HTTPException(status_code=404, detail="Furniture not found")
    furniture.ProductName = new_data.ProductName
    furniture.description = new_data.description
    furniture.image = new_data.image
    # furniture.brand = new_data.brand
    furniture.price = new_data.price
    furniture.stock = new_data.stock
    furniture.subcategory_id = new_data.subcategory_id
    furniture.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(furniture)
    return furniture


@furnitures_router.delete("/furnitures/{furniture_id}")
def delete_furniture(furniture_id: int, db: Session = Depends(get_db),    user=Depends(get_current_user)):
    furniture = db.query(Furniture).filter(Furniture.ProductID == furniture_id).first()
    if not furniture:
        raise HTTPException(status_code=404, detail="Furniture not found")
    db.delete(furniture)
    db.commit()
    return {"message": "Furniture deleted successfully"}


# --- Category Endpoints ---
@furnitures_router.get("/categories", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@furnitures_router.post("/categories", response_model=CategoryOut)
def add_category(category: CategoryInDB, db: Session = Depends(get_db),user=Depends(get_current_user)):
    new_category = Category(
        name=category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# --- SubCategory Endpoints ---
@furnitures_router.get("/subcategories", response_model=List[SubCategoryOut])
def get_subcategories(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()


@furnitures_router.post("/subcategories", response_model=SubCategoryOut)
def add_subcategory(subcategory: SubCategoryInDB, db: Session = Depends(get_db),user=Depends(get_current_user)):
    new_subcategory = SubCategory(
        name=subcategory.name,
        category_id=subcategory.category_id
    )
    db.add(new_subcategory)
    db.commit()
    db.refresh(new_subcategory)
    return new_subcategory