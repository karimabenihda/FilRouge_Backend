from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class RequestMsg(BaseModel):
    query: str


class ResponseMsg(BaseModel):
    reply: str


