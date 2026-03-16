from sqlalchemy import Column, String, Integer,Enum, DateTime, Float, ForeignKey,Date
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


class Sale(Base):
    __tablename__ = "sales"

    row_id = Column(Integer, primary_key=True, index=True)

    order_id = Column(String)
    order_date = Column(Date)
    ship_date = Column(Date)
    ship_mode = Column(String)

    customer_id = Column(String)
    customer_name = Column(String)
    segment = Column(String)

    city = Column(String)
    region = Column(String)

    product_id = Column(String)
    category = Column(String)
    sub_category = Column(String)
    product_name = Column(String)

    sales = Column(Float)
    quantity = Column(Integer)
    discount = Column(Float)
    profit = Column(Float)

    season = Column(String)
    brand = Column(String)