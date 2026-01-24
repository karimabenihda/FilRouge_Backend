from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserInDB(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: Optional[str] = "client"
    created_at:datetime
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    role: str
    created_at: datetime
    
class Token(BaseModel):
    access_token: str
    token_type: str