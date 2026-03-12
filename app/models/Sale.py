from sqlalchemy import Column, String, Integer,Enum, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.core.database import Base
from sqlalchemy.orm import relationship
import enum


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("furnitures.ProductID"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    subtotal = Column(Float, nullable=False, default=0.0)
    discount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Named "product" so Pydantic's CartResponse.product field is populated automatically
    product = relationship("Furniture", foreign_keys=[product_id], lazy="joined")
    user = relationship("User", backref="cart_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("furnitures.ProductID"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")
    totalprice = Column(Float, nullable=False)
    product_qte = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    furniture = relationship("Furniture", backref="order_items")
    user = relationship("User", backref="orders")





class PaymentStatus(str, enum.Enum):
    pending   = "pending"
    completed = "completed"
    failed    = "failed"
    refunded  = "refunded"


class PaymentMethod(str, enum.Enum):
    credit_card = "credit_card"
    debit_card  = "debit_card"
    paypal      = "paypal"
    cash        = "cash"


class Payment(Base):
    __tablename__ = "payments"

    id             = Column(Integer, primary_key=True, index=True)
    order_id       = Column(Integer, ForeignKey("orders.id"), nullable=False)
    customer_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount         = Column(Float, nullable=False)
    method         = Column(Enum(PaymentMethod), nullable=False, default=PaymentMethod.credit_card)
    status         = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    card_last4     = Column(String(4), nullable=True)
    cardholder     = Column(String, nullable=True)
    created_at     = Column(DateTime, default=datetime.utcnow)

    order    = relationship("Order", backref="payment")
    customer = relationship("User",  backref="payments")






# class FurnitureSales(Base):
    # __tablename__="recommendation"
    # RowID =Column(Integer,  nullable=False)
    # OrderID =Column(String,nullable=False)
    # OrderDate =Column(String,nullable=False)
    # ShipDate =Column(String,nullable=False)
    # ShipMode =Column(String,nullable=False)
    # CustomerID =Column(String,nullable=False)
    # CustomerName=Column(String,nullable=False)
    # Segment =Column(String,nullable=False)
    # Country =Column(String,nullable=False)
    # City =Column(String,nullable=False)
    # State =Column(String,nullable=False)
    # PostalCode=Column(Integer,  nullable=False)
    # Region =Column(String,nullable=False)
    # ProductID =Column(String,nullable=False)
    # Category =Column(String,nullable=False)
    # SubCategory =Column(String,nullable=False)
    # ProductName =Column(String,nullable=False)
    # Sales =Column(Float,  nullable=False)
    # Quantity  =Column(Integer,  nullable=False)
    # Discount=Column(Float,  nullable=False)
    # Profit  =Column(Float,  nullable=False)
    # season =Column(String,nullable=False)
    # brand =Column(String,nullable=False)

# class Sales(Base):
#     __tablename__="sales"
#     id = Column(Integer, primary_key=True, autoincrement=True)  # internal PK
#     OrderID = Column(String(50), nullable=False)
#     OrderDate = Column(DateTime, nullable=False)
#     ShipDate = Column(DateTime, nullable=False)
#     ShipMode = Column(String(50), nullable=False)
#     CustomerID = Column(String(50), nullable=False)
#     CustomerName = Column(String(100), nullable=False)
#     Segment = Column(String(50), nullable=False)
#     City = Column(String(50), nullable=False)
#     Region = Column(String(50), nullable=False)
#     ProductID = Column(String(50), nullable=False)
#     Category = Column(String(50), nullable=False)
#     SubCategory = Column(String(50), nullable=False)
#     ProductName = Column(String(100), nullable=False)
#     Sales = Column(Float, nullable=False)
#     Quantity = Column(Integer, nullable=False)
#     Discount = Column(Float, nullable=True)
#     Profit = Column(Float, nullable=True)
#     season = Column(String(20), nullable=True)
#     brand = Column(String(50), nullable=True)
    
    