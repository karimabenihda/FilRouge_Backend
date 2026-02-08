from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.Furniture import Furniture ,Category
from app.schemas.Furniture import FurnitureInDB, CategoryInDB ,FurnitureUpdate
from datetime import datetime

sales_router  = APIRouter()

@sales_router.get('/get_furniturs')
def get_furniturs(db: Session = Depends(get_db)):
    result=db.query(Furniture).all()
    return result


@sales_router.post('/add_furniturs')
def add_furniturs(furniture:FurnitureInDB ,db: Session = Depends(get_db)):
    
    new_furnitures=Furniture(
        name=furniture.name,
        description=furniture.description,
        image=furniture.image,
        price=furniture.price,
        stock=furniture.stock,
        id_category=furniture.id_category,
        created_at=datetime.now(),
                         )
    db.add(new_furnitures) 
    db.commit()
    db.refresh(new_furnitures)
    return {"message": "Furniture created successfully", "price": new_furnitures.id}

@sales_router.delete('/delete_furniture/{furniture_id}')
def delete_furniture(furniture_id:int ,db: Session = Depends(get_db)):
    furniture=db.query(Furniture).filter(Furniture.id==furniture_id).first()
    if not furniture:
        raise HTTPException(status_code=404, detail="Furniture not found")
    db.delete(furniture)
    db.commit()
    return {"msg":"Furniture deleted successfullt"}



@sales_router.put("/update_furniture/{furniture_id}")
def update_furniture(
    furniture_id: int,
    new_data: FurnitureUpdate,
    db: Session = Depends(get_db)
):
    furniture = db.query(Furniture).filter(Furniture.id == furniture_id).first()

    if not furniture:
        raise HTTPException(status_code=404, detail="Furniture not found")

    furniture.name = new_data.name
    furniture.description = new_data.description
    furniture.image = new_data.image
    furniture.price = new_data.price
    furniture.stock = new_data.stock
    furniture.id_category = new_data.id_category
    furniture.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(furniture)

    return {
        "message": "Furniture updated successfully",
        "furniture_id": furniture.id
    }




#____________Category______________

@sales_router.get('/get_category')
def get_category(db: Session = Depends(get_db)):
    result=db.query(Category).all()
    return result

@sales_router.post('/add_categories')
def add_categories(category:CategoryInDB ,db: Session = Depends(get_db)):
    categories=Category(
        name=category.name,
        description=category.description,
                         )
    db.add(categories) 
    db.commit()
    db.refresh(categories)
    return categories  
