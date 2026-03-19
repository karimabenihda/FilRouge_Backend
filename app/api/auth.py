from app.schemas.User import UserInDB, Token, UserLogin,UserUpdate,UserOut
from app.models.User import User
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import os
from app.core.database import get_db
from dotenv import load_dotenv 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()
from pathlib import Path
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
CLIENT_ID=os.getenv("CLIENT_ID")


auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----- Helpers -----
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = None):
    """Génère un JWT pour ton application"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        print(f"JWT Error: {str(e)}") # Log the error on the server
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication error")


# ----- Login -----
@auth_router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": db_user.email,
        "user_id": db_user.id,
        "role": db_user.role,
        "firstname": db_user.firstname,
        "lastname": db_user.lastname
    })

    return {"access_token": token, "token_type": "bearer"}


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
        # created_at = datetime.utcnow(),
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

# @auth_router.get("/me", response_model=UserOut)
# def get_me(db: Session = Depends(get_db), user=Depends(get_current_user)):
#     existing = db.query(User).filter(User.id == user.id).first()
#     if not existing:
#         raise HTTPException(status_code=404, detail="User not found")
#     return existing

@auth_router.get("/me", response_model=UserOut)
def get_me(db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_id = user["user_id"]  # ← JWT stores it as "user_id" not "id"
    existing = db.query(User).filter(User.id == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    return existing

@auth_router.post("/logout")
def logout():
    return {"message": "Logged out"}
