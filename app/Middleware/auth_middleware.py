from fastapi import Depends, HTTPException, Request
from jose import jwt
from dotenv import load_dotenv 
load_dotenv()
import os 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(request: Request):

    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(401, "Token missing")

    token = token.replace("Bearer ", "")

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload


def admin_required(user=Depends(get_current_user)):

    if user["role"] != "admin":
        raise HTTPException(403, "Admin access required")

    return user
