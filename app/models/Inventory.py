from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("furnitures.ProductID"), nullable=False)
    change_quantity = Column(Integer, nullable=False)  # + for restock, - for sales/adjustments
    reason = Column(String(100), nullable=False)       # "restock", "adjustment", "sale", etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to Furniture
    product = relationship("Furniture", backref="inventory_logs")
