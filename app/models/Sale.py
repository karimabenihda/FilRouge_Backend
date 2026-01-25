from sqlalchemy import Column, String, Integer, DateTime,Float,ForeignKey,ClauseList
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from core.database import Base
from sqlalchemy.orm import relationship


   
class Recommendation(Base):
    __tablename__="recommendation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliend_id=Column(Integer,  nullable=False)
    furnitures_id=Column(Integer,ClauseList,  nullable=False)

class Prediction(Base):
    __tablename__="predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    month=Column(DateTime,  nullable=False)
    expected_sales=Column(Float,  nullable=False)
    threshold=Column(Float,  nullable=False)
    risk_level=Column(String,  nullable=False)
    plans=Column(String, nullable=False)


class Sale(Base):
    __tablename__="sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    furniture_id=Column(Integer,nullable=False)
    quantity=Column(Integer,  nullable=False)
    total_price=Column(Float,  nullable=False)
    date=Column(DateTime,nullable=False )
