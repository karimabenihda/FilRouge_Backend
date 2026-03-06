from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ElenaSchema(BaseModel):
    model_name: str
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True


class MessageSchema(BaseModel):
    session_id: int
    sender: str
    message: str
    end_time: datetime

    class Config:
        orm_mode = True


class SessionSchema(BaseModel):
    client_id: int
    start_time: datetime
    end_time: datetime
    messages: Optional[List[MessageSchema]] = []

    class Config:
        orm_mode = True


class InteractionSchema(BaseModel):
    client_id: int
    furniture_id: int
    type: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


class IntentSchema(BaseModel):
    name: str
    confidence: float

    class Config:
        orm_mode = True