# from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserInDB(BaseModel):
    firstname: str
    lastname: str
    # email: EmailStr
    email: str
    password: str
    role: Optional[str] = "user"
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    role: str
    created_at: datetime
    
class Token(BaseModel):
    access_token: str
    token_type: str