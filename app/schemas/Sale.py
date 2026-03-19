from pydantic import BaseModel,Field, ConfigDict
from datetime import datetime,date
from typing import Optional
from enum import Enum
from typing import List

# ──────────────── FURNITURE (nested in cart) ────────────────

class FurnitureInfo(BaseModel):
    ProductID: int
    ProductName: str
    price: float
    image: Optional[str] = None

    class Config:
        from_attributes = True

# ──────────────── CART ────────────────

class CartBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int
    subtotal: float
    discount: float = 0.0

class CartCreate(CartBase):
    pass

class CartUpdate(BaseModel):
    quantity: Optional[int] = None
    subtotal: Optional[float] = None
    discount: Optional[float] = None

class CartResponse(CartBase):
    id: int
    created_at: datetime
    product: Optional[FurnitureInfo] = None   # ✅ Correct nested schema

    class Config:
        from_attributes = True

# ──────────────── ORDER ────────────────

class OrderBase(BaseModel):
    product_id: int
    customer_id: int
    status: str = "pending"
    totalprice: float
    product_qte: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    totalprice: Optional[float] = None
    product_qte: Optional[int] = None

class OrderResponse(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


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
        from_attributes=True
        
        
from enum import Enum


class PaymentStatus(str, Enum):
    pending   = "pending"
    completed = "completed"
    failed    = "failed"
    refunded  = "refunded"


class PaymentMethod(str, Enum):
    credit_card = "credit_card"
    debit_card  = "debit_card"
    paypal      = "paypal"
    cash        = "cash"


# ──────────────── REQUEST ────────────────

class PaymentCreate(BaseModel):
    cardholder:  str
    card_number: str = Field(..., min_length=16, max_length=16)
    expiry:      str = Field(..., pattern=r"^\d{2}/\d{2}$")   # MM/YY
    cvv:         str = Field(..., min_length=3, max_length=4)
    method:      PaymentMethod = PaymentMethod.credit_card


# ──────────────── RESPONSE ────────────────

class PaymentResponse(BaseModel):
    id:          int
    order_id:    int
    customer_id: int
    amount:      float
    method:      PaymentMethod
    status:      PaymentStatus
    card_last4:  Optional[str]
    cardholder:  Optional[str]
    created_at:  datetime

    class Config:
        from_attributes = True


# ──────────────── ORDER RESPONSE (returned alongside payment) ────────────────

class OrderSummaryResponse(BaseModel):
    order_ids:   list[int]
    total_price: float
    payment:     PaymentResponse

    class Config:
        from_attributes = True


class ProductInfo(BaseModel):
    ProductID:   Optional[int] = None
    ProductName: Optional[str] = None
    name:        Optional[str] = None
    price:       Optional[float] = None
    image:       Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OrderDetailResponse(BaseModel):
    id:          int
    product_id:  int
    customer_id: int
    status:      str
    totalprice:  float
    product_qte: int
    created_at:  datetime
    product:     Optional[ProductInfo] = None
    model_config = ConfigDict(from_attributes=True)

class PaymentInfo(BaseModel):
    id:             Optional[int]      = None
    amount:         Optional[float]    = None
    method:         Optional[str]      = None
    payment_method: Optional[str]      = None
    status:         Optional[str]      = None
    card_last4:     Optional[str]      = None
    created_at:     Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class OrderTrackingResponse(BaseModel):
    orders:      List[OrderDetailResponse]
    total_price: float
    payment:     Optional[PaymentInfo] = None
    model_config = ConfigDict(from_attributes=True)

class AdminOrderTrackingResponse(BaseModel):
    orders:      List[OrderDetailResponse]
    total_price: float
    payment:     Optional[PaymentInfo] = None



class AdminOrderItem(BaseModel):
    id:            int
    product_id:    int
    customer_id:   int
    status:        str
    totalprice:    float
    product_qte:   int
    created_at:    datetime
    product_name:  Optional[str] = None
    product_image: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class StatusUpdateResponse(BaseModel):
    order_id:   int
    new_status: str



class SaleCreate(BaseModel):
    row_id: int
    order_id: str
    order_date: date
    ship_date: date
    ship_mode: str

    customer_id: str
    customer_name: str
    segment: str

    city: str
    region: str

    product_id: str
    category: str
    sub_category: str
    product_name: str

    sales: float
    quantity: int
    discount: float
    profit: float

    season: str
    brand: str
    
    
class MonthlySalesItem(BaseModel):
    year:         int
    month:        int
    total_sales:  float
    total_profit: float
    total_orders: int

class YearlySalesItem(BaseModel):
    year:         int
    total_sales:  float
    total_profit: float
    total_orders: int
    months:       List[MonthlySalesItem]