from sqlalchemy import Column, String, Integer, DateTime,Float,ForeignKey,ClauseList
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from core.database import Base
from sqlalchemy.orm import relationship


class FurnitureSales(Base):
    __tablename__="recommendation"
    RowID =Column(Integer,  nullable=False)
    OrderID =Column(String,nullable=False)
    OrderDate =Column(String,nullable=False)
    ShipDate =Column(String,nullable=False)
    ShipMode =Column(String,nullable=False)
    CustomerID =Column(String,nullable=False)
    CustomerName=Column(String,nullable=False)
    Segment =Column(String,nullable=False)
    Country =Column(String,nullable=False)
    City =Column(String,nullable=False)
    State =Column(String,nullable=False)
    PostalCode=Column(Integer,  nullable=False)
    Region =Column(String,nullable=False)
    ProductID =Column(String,nullable=False)
    Category =Column(String,nullable=False)
    SubCategory =Column(String,nullable=False)
    ProductName =Column(String,nullable=False)
    Sales =Column(Float,  nullable=False)
    Quantity  =Column(Integer,  nullable=False)
    Discount=Column(Float,  nullable=False)
    Profit  =Column(Float,  nullable=False)
    season =Column(String,nullable=False)
    brand =Column(String,nullable=False)

class Sales(Base):
    __tablename__="sales"
    id = Column(Integer, primary_key=True, autoincrement=True)  # internal PK
    OrderID = Column(String(50), nullable=False)
    OrderDate = Column(DateTime, nullable=False)
    ShipDate = Column(DateTime, nullable=False)
    ShipMode = Column(String(50), nullable=False)
    CustomerID = Column(String(50), nullable=False)
    CustomerName = Column(String(100), nullable=False)
    Segment = Column(String(50), nullable=False)
    City = Column(String(50), nullable=False)
    Region = Column(String(50), nullable=False)
    ProductID = Column(String(50), nullable=False)
    Category = Column(String(50), nullable=False)
    SubCategory = Column(String(50), nullable=False)
    ProductName = Column(String(100), nullable=False)
    Sales = Column(Float, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Discount = Column(Float, nullable=True)
    Profit = Column(Float, nullable=True)
    season = Column(String(20), nullable=True)
    brand = Column(String(50), nullable=True)
    
    