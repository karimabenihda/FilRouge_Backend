from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Elena(Base):
    __tablename__ = "elena"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    messages = relationship("Message", back_populates="session")
    users = relationship("User", back_populates="session")  # assuming you have a User model


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    sender = Column(String, nullable=False)
    message = Column(String, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    session = relationship("Session", back_populates="messages")


class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, nullable=False)
    furniture_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Intent(Base):
    __tablename__ = "intents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)