from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryInDB(BaseModel):
    name:str


class FurnitureInDB(BaseModel):
    name:str
    description:str
    image:str
    price:float
    stock:int
    views:int
    category:CategoryInDB
    created_at:datetime

class FurnitureUpdate(BaseModel):
    name:str
    description:str
    image:str
    price:float
    stock:int
    views:int
    category:CategoryInDB
    updated_at:datetime
