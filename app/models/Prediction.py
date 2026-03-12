from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

   
class Recommendation(Base):
    __tablename__ = "recommendation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(String, nullable=False)
    ProductID = Column(String, nullable=False)


class SalesPrediction(Base):
    __tablename__="sales_predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    month=Column(DateTime,  nullable=False)
    expected_sales=Column(Float,  nullable=False)
    threshold=Column(Float,  nullable=False)
    risk_level=Column(String,  nullable=False)
    plans=Column(String, nullable=False)



