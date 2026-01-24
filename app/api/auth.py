from schemas.User import UserInDB, Token, UserLogin
from models.User import User
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import os
from core.database import get_db
from dotenv import load_dotenv 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # convert to int

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----- Helpers -----
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----- Login -----
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


# ----- Register -----
@router.post("/register")
def register(user: UserInDB, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
        created_at=datetime.utcnow(),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.id}
