from app.schemas.User import UserInDB,Token
from passlib.context import CryptContext
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import os
from app.core.database import get_db
from dotenv import load_dotenv 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router=APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=Token)
async def login(User:UserInDB,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==UserInDB.email).first()
    if not user or not verify_password(User.password,user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user and verify_password(User.password,user.password):
        token=create_access_token({"sub":user.email})
        return {"access_token":token, "token_type":"bearer"}