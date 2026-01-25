
from sqlalchemy import Column, String, Integer, DateTime,Float,ForeignKey,ClauseList
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from core.database import Base
from sqlalchemy.orm import relationship


class Elena(Base):
    __tablename__="elena"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name=Column(String,  nullable=False)
    answer=Column(String,  nullable=False)
    created_at=Column(DateTime,nullable=False)

class Message(Base):
    __tablename__="messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id=Column(Integer,  nullable=False)
    sender=Column(String, nullable=False )
    message=Column(String, nullable=False )
    end_time=Column(DateTime, nullable=False )
    
    sessions=relationship('Session',back_populates="messages")


class Session(Base):
    __tablename__="sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliend_id=Column(Integer,  nullable=False)
    start_time=Column(DateTime,  nullable=False)    
    end_time=Column(DateTime,  nullable=False)
    
    messages=relationship('Message',back_populates="session")
    users=relationship('User',back_populates="session")


class Interaction(Base):
    __tablename__="interactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliend_id=Column(Integer,  nullable=False)
    furniture_id=Column(Integer,  nullable=False)
    type=Column(String,  nullable=False)
    content=Column(String,  nullable=False)
    created_at=Column(DateTime,  nullable=False)

class Intent(Base):
    __tablename__="interactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String,  nullable=False)
    confidence=Column(Float,  nullable=False)
    