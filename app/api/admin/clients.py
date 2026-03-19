from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from app.core.database import get_db
from app.models.User import User
from app.schemas.User import UserInDB, UserOut
from app.api.auth import get_current_user
from typing import List
import bcrypt

users_router = APIRouter()

# --- Get all users ---
@users_router.get("/get_users", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(User).all()

# --- Create user ---
@users_router.post("/add_user", response_model=UserOut)
def create_user(data: UserInDB, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    new_user = User(
        firstname=data.firstname,
        lastname=data.lastname,
        email=data.email,
        password=hashed,
        role=data.role or "client",
        created_at=datetime.utcnow(),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- Delete user ---
# @users_router.delete("/delete_user/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     target = db.query(User).filter(User.id == user_id).first()
#     if not target:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(target)
#     db.commit()
#     return {"message": "User deleted successfully"}

# --- Update user role ---
@users_router.patch("/update_user/{user_id}/role")
def update_role(user_id: int, role: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    target.role = role
    target.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Role updated"}

# --- Stats: users per month for current year ---
@users_router.get("/stats/monthly")
def monthly_stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    current_year = datetime.utcnow().year
    results = (
        db.query(
            extract("month", User.created_at).label("month"),
            func.count(User.id).label("count"),
        )
        .filter(extract("year", User.created_at) == current_year)
        .group_by("month")
        .order_by("month")
        .all()
    )
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data = {months[int(r.month) - 1]: int(r.count) for r in results}
    return [{"month": m, "users": data.get(m, 0)} for m in months]

# --- Stats: total users ---
@users_router.get("/stats/total")
def total_stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    total = db.query(func.count(User.id)).scalar()
    admins = db.query(func.count(User.id)).filter(User.role == "admin").scalar()
    clients = db.query(func.count(User.id)).filter(User.role == "client").scalar()
    return {"total": total, "admins": admins, "clients": clients}