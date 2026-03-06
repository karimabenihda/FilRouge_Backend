from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SaleSchema(BaseModel):
    OrderID: str
    OrderDate: datetime
    ShipDate: datetime
    ShipMode: str
    CustomerID: str
    CustomerName: str
    Segment: str
    City: str
    Region: str
    ProductID: str
    Category: str
    SubCategory: str
    ProductName: str
    Sales: float
    Quantity: int
    Discount: Optional[float] = None
    Profit: Optional[float] = None
    season: Optional[str] = None
    brand: Optional[str] = None

    class Config:
        orm_mode = True