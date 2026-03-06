from sqlalchemy import Column, String, Integer, DateTime,Float,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.core.database import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    sub_category = Column(String(50), nullable=True)
    
    furnitures = relationship("Furniture", back_populates="category")


class Furniture(Base):
    __tablename__ = "furnitures"
    
    ProductID = Column(Integer, primary_key=True, autoincrement=True)
    ProductName = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    views = Column(Integer, nullable=True)
    
    id_category = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship back to Category
    category = relationship("Category", back_populates="furnitures")