from pydantic import BaseModel
from datetime import datetime


class CategoryInDB(BaseModel):
    name:str
    description:str


class FurnitureInDB(BaseModel):
    name:str
    description:str
    image:str
    price:float
    stock:int
    id_category: int

class FurnitureUpdate(BaseModel):
    name:str
    description:str
    image:str
    price:float
    stock:int
    id_category:int
