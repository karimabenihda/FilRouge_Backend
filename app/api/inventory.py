from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.Furniture import Furniture
from app.models.Inventory import InventoryLog
from app.schemas.Inventory import InventoryLogOut, StockUpdate
from app.Middleware.auth_middleware import admin_required, get_current_user

inventory_router = APIRouter()

@inventory_router.get("/status")
def get_stock_status(db: Session = Depends(get_db)):
    """Get current stock levels for all furnitures"""
    results = db.query(
        Furniture.ProductID,
        Furniture.ProductName,
        Furniture.stock,
        Furniture.price,   # ✅ add this
        Furniture.image    # ✅ add this
    ).all()
    return [
        {
            "ProductID": row.ProductID,
            "ProductName": row.ProductName,
            "stock": row.stock,
            "price": row.price,   # ✅ add this
            "image": row.image    # ✅ add this
        }
        for row in results
    ]
@inventory_router.post("/update")
def update_stock(data: StockUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Update stock level and record it in inventory logs"""
    product = db.query(Furniture).filter(Furniture.ProductID == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    old_stock = product.stock
    change = data.new_stock - old_stock

    # Update product stock
    product.stock = data.new_stock

    # Create log entry
    log_entry = InventoryLog(
        product_id=data.product_id,
        change_quantity=change,
        reason=data.reason
    )

    db.add(log_entry)
    db.commit()
    db.refresh(product)

    return {"message": "Stock updated", "new_stock": product.stock, "change": change}

@inventory_router.get("/logs", response_model=List[InventoryLogOut])
def get_inventory_logs(db: Session = Depends(get_db)):
    """Get history of stock movements"""
    return db.query(InventoryLog).order_by(InventoryLog.created_at.desc()).all()
