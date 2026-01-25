from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.Furniture import Furniture ,Category
from schemas.Furniture import FurnitureInDB, CategoryInDB ,FurnitureUpdate
from datetime import datetime

router = APIRouter()

@router.get('/get_furniturs')
def get_furniturs(db: Session = Depends(get_db)):
    result=db.query(Furniture)
    return result


@router.post('/add_furniturs')
def add_furniturs(furniture=FurnitureInDB ,db: Session = Depends(get_db)):
    new_furnitures=Furniture(
        name=furniture.name,
        description=furniture.description,
        image=furniture.image,
        price=furniture.price,
        stock=furniture.stock,
        views=furniture.views,
        id_category=furniture.id_category,
        created_at=datetime.utcnow,
                         )
    db.add(new_furnitures) 
    db.commit()
    db.refresh(new_furnitures)
    return new_furnitures  

@router.delete('/delete_furniture/{furniture_id}')
def delete_furniture(furniture_id:int ,db: Session = Depends(get_db)):
    furniture=db.query(Furniture).filter(Furniture.id==furniture_id).first()
    if not furniture:
        raise HTTPException(status_code=404, detail="Furniture not found")
    db.delete(furniture)
    db.commit()
    return {"msg":"Furniture deleted successfullt"}


@router.put('/update_furniture/{furniture_id}')
def update_furniture(furniture_id:int ,new_data:FurnitureUpdate,db: Session = Depends(get_db)):
    furniture=db.query(Furniture).filter(Furniture.id==furniture_id).first()
    if not furniture:
        raise HTTPException(status_code=404, detail="Furniture not found")
    new_furniture_info={
            furniture.name:FurnitureUpdate.name,
            furniture.description:FurnitureUpdate.description,
            furniture.image:FurnitureUpdate.image,
            furniture.price:FurnitureUpdate.price,
            furniture.stock:FurnitureUpdate.stock,
            furniture.views:FurnitureUpdate.views,
            furniture.category:CategoryInDB,
            furniture.updated_at:datetime
    }
    
    db.delete(new_furniture_info)
    db.commit()
    return {"msg":"Furniture updated successfullt"}

#____________Category______________

@router.get('/get_category')
def get_category(db: Session = Depends(get_db)):
    result=db.query(Category)
    return result

@router.post('/add_categories')
def add_categories(category=CategoryInDB ,db: Session = Depends(get_db)):
    categories=Category(
        name=category.name,
        description=category.description,
                         )
    db.add(categories) 
    db.commit()
    db.refresh(categories)
    return categories  
