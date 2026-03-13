from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.models.Sale import Order,Payment
from app.models.Furniture import Furniture
from app.api.auth import get_current_user
from app.schemas.Sale import OrderTrackingResponse,AdminOrderItem,StatusUpdateResponse
from app.schemas.Sale import OrderDetailResponse,ProductInfo,PaymentInfo
orders_router = APIRouter(prefix="/api/orders", tags=["orders"])

# ──────────────── STATUS FLOW ────────────────

STATUS_FLOW = ["pending", "confirmed", "preparing", "shipped", "delivering", "delivered"]

# ──────────────── SCHEMAS ────────────────

# ──────────────── GET ALL ORDERS — ADMIN ────────────────
# THIS is the endpoint the frontend calls on mount:
#   GET /api/sales/orders/all
# It returns a flat list where product info is hoisted onto each row.

@orders_router.get("/orders/all", response_model=List[AdminOrderItem])
def get_all_orders(
    db:   Session = Depends(get_db),
    user              = Depends(get_current_user),
):
    orders = (
        db.query(Order)
        .order_by(desc(Order.created_at))
        .all()
    )

    result: List[AdminOrderItem] = []
    for o in orders:
        product = (
            db.query(Furniture)
            .filter(Furniture.ProductID == o.product_id)
            .first()
        )
        result.append(AdminOrderItem(
            id            = o.id,
            product_id    = o.product_id,
            customer_id   = o.customer_id,
            status        = o.status,
            totalprice    = o.totalprice,
            product_qte   = o.product_qte,
            created_at    = o.created_at,
            # ↓ adjust these attribute names to match your Furniture model columns
            product_name  = getattr(product, "Name",  None),
            product_image = getattr(product, "Image", None),
        ))

    return result


# ──────────────── GET ORDERS FOR ONE CUSTOMER ────────────────
# Called by the detail dialog to fetch payment info:
#   GET /api/sales/get_orders/{customer_id}

@orders_router.get("/get_orders/{customer_id}", response_model=OrderTrackingResponse)
def get_orders(
    customer_id: int,
    db:          Session = Depends(get_db),
    user                 = Depends(get_current_user),
):
    orders = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(desc(Order.created_at))
        .all()
    )
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    order_details = []
    for o in orders:
        product = db.query(Furniture).filter(Furniture.ProductID == o.product_id).first()
        order_details.append(OrderDetailResponse(
            id          = o.id,
            product_id  = o.product_id,
            customer_id = o.customer_id,
            status      = o.status,
            totalprice  = o.totalprice,
            product_qte = o.product_qte,
            created_at  = o.created_at,
            product     = ProductInfo(
                name  = getattr(product, "Name",  None),
                image = getattr(product, "Image", None),
            ) if product else None,
        ))

    payment = (
        db.query(Payment)
        .filter(Payment.customer_id == customer_id)
        .order_by(desc(Payment.created_at))
        .first()
    )

    return OrderTrackingResponse(
        orders      = order_details,
        total_price = sum(o.totalprice for o in orders),
        payment     = PaymentInfo.model_validate(payment) if payment else None,
    )


# ──────────────── ADVANCE ORDER STATUS ────────────────
# PUT /api/sales/{order_id}/status  →  { order_id, new_status }

@orders_router.put("/{order_id}/status", response_model=StatusUpdateResponse)
def update_order_status(
    order_id: int,
    db:       Session = Depends(get_db),
    user              = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Cannot advance a cancelled order")

    current_index = STATUS_FLOW.index(order.status) if order.status in STATUS_FLOW else 0
    if current_index < len(STATUS_FLOW) - 1:
        order.status = STATUS_FLOW[current_index + 1]
        db.commit()
        db.refresh(order)

    return StatusUpdateResponse(order_id=order.id, new_status=order.status)



@orders_router.put("/{order_id}/cancel", response_model=StatusUpdateResponse)
def cancel_order(
    order_id: int,
    db:       Session = Depends(get_db),
    user              = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status in ["shipped", "delivering", "delivered"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel an order that is already '{order.status}'",
        )

    if order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Order is already cancelled")

    order.status = "cancelled"
    db.commit()
    db.refresh(order)

    return StatusUpdateResponse(order_id=order.id, new_status="cancelled")