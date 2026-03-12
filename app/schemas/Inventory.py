from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InventoryLogBase(BaseModel):
    product_id: int
    change_quantity: int
    reason: str

class InventoryLogCreate(InventoryLogBase):
    pass

class InventoryLogOut(InventoryLogBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class StockUpdate(BaseModel):
    product_id: int
    new_stock: int
    reason: Optional[str] = "Manual update"
