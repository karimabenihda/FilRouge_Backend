from app.schemas.User import UserInDB, Token, UserLogin,UserUpdate
from app.models.User import User
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from app.schemas.User import Token,GoogleToken
import os
from app.core.database import get_db
from dotenv import load_dotenv 
from google.oauth2 import id_token
from google.auth.transport import requests



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # convert to int
CLIENT_ID=os.getenv("CLIENT_ID")


auth_router = APIRouter()
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

def create_access_token(data: dict, expires_delta: int = None):
    """Génère un JWT pour ton application"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ----- Login -----
@auth_router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


# ----- google-login -----
@auth_router.post("/google-login")
def google_login(
    token_data: GoogleToken,
    db: Session = Depends(get_db)
):
    try:
        idinfo = id_token.verify_oauth2_token(
            token_data.token,
            requests.Request(),
            CLIENT_ID
        )

        # Security check
        if idinfo["aud"] != CLIENT_ID:
            raise ValueError("Invalid audience")

        email = idinfo.get("email")
        google_id = idinfo.get("sub")
        firstname = idinfo.get("given_name", "")
        lastname = idinfo.get("family_name", "")

        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Google")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                google_id=google_id,
                role="client",
                auth_provider="google"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "firstname": user.firstname,
                "role": user.role
            }
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")


# ----- Register -----
@auth_router.post("/register")
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

# ----- Update -----
@auth_router.put("/update_user/{user_id}")
def update_user(user_id: int,user: UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not exists")
    
    existing_user.firstname=user.firstname
    existing_user.lastname=user.lastname
    existing_user.email=user.email
    existing_user.password=hash_password(user.password)
    existing_user.updated_at=datetime.utcnow()
    db.commit()
    db.refresh(existing_user)
    
    return {"message": "User updated successfully", "user_id": existing_user.firstname}



@auth_router.post("/logout")
def logout():
    return {"message": "Logged out"}
