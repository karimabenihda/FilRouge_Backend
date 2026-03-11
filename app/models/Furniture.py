from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


# ---------------- CATEGORY ----------------

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    # Category → SubCategories
    subcategories = relationship(
        "SubCategory",
        back_populates="category",
        cascade="all, delete-orphan"
    )


# ---------------- SUBCATEGORY ----------------

class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # SubCategory → Category
    category = relationship(
        "Category",
        
        back_populates="subcategories"
    )

    # SubCategory → Furnitures
    furnitures = relationship(
        "Furniture",
        back_populates="subcategory",
        cascade="all, delete-orphan"
    )


# ---------------- FURNITURE ----------------

class Furniture(Base):
    __tablename__ = "furnitures"

    ProductID = Column(Integer, primary_key=True, autoincrement=True)
    ProductName = Column(String(50), nullable=False)

    description = Column(String, nullable=True)
    image = Column(String, nullable=False)
    # brand = Column(String, nullable=False)

    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    views = Column(Integer, nullable=True)

    subcategory_id = Column(
        Integer,
        ForeignKey("subcategories.id"),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Furniture → SubCategory
    subcategory = relationship(
        "SubCategory",
        back_populates="furnitures"
    )