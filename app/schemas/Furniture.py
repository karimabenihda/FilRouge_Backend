from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ---------------- CATEGORY ----------------

class CategoryBase(BaseModel):
    name: str


class CategoryInDB(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# ---------------- SUBCATEGORY ----------------

class SubCategoryBase(BaseModel):
    name: str
    category_id: int


class SubCategoryInDB(SubCategoryBase):
    pass


class SubCategoryOut(SubCategoryBase):
    id: int
    category: Optional[CategoryOut] = None

    class Config:
        orm_mode = True


# ---------------- FURNITURE ----------------

class FurnitureBase(BaseModel):
    ProductName: str
    description: Optional[str] = None
    image: str
    # brand:str
    price: float
    stock: int
    subcategory_id: int


# Create furniture
class FurnitureInDB(FurnitureBase):
    pass


# Update furniture
class FurnitureUpdate(BaseModel):
    ProductName: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    subcategory_id: Optional[int] = None


# Response model
class FurnitureOut(FurnitureBase):
    ProductID: int
    views: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    subcategory: Optional[SubCategoryOut] = None

    class Config:
        orm_mode = True