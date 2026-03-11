from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.Sale import Cart,Payment, PaymentStatus,Order,PaymentMethod,Payment

from app.models.Furniture import Furniture
from app.schemas.Sale import CartCreate, CartResponse, CartUpdate,PaymentCreate, OrderSummaryResponse, PaymentResponse,PaymentStatus,PaymentMethod,PaymentCreate,PaymentResponse,OrderSummaryResponse,ProductInfo,OrderDetailResponse,PaymentInfo,OrderTrackingResponse
from typing import List


sales_router = APIRouter()


# ──────────────── GET CART BY CUSTOMER ────────────────

@sales_router.get("/{customer_id}", response_model=List[CartResponse])
def get_cart(customer_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.customer_id == customer_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart_items


# ──────────────── ADD TO CART ────────────────

@sales_router.post("/add", response_model=CartResponse)
def add_to_cart(cart_data: CartCreate, db: Session = Depends(get_db)):

    # Check product exists — utilise Furniture et ProductID
    product = db.query(Furniture).filter(
        Furniture.ProductID == cart_data.product_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if product already in cart
    existing_item = db.query(Cart).filter(
        Cart.customer_id == cart_data.customer_id,
        Cart.product_id == cart_data.product_id
    ).first()

    if existing_item:
        # Produit déjà dans le cart → augmente qty et recalcule subtotal
        existing_item.quantity += cart_data.quantity
        existing_item.subtotal = existing_item.quantity * product.price
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Nouveau produit → crée un item
        subtotal = cart_data.quantity * product.price
        new_item = Cart(
            product_id=cart_data.product_id,
            customer_id=cart_data.customer_id,
            quantity=cart_data.quantity,
            subtotal=subtotal,
            discount=cart_data.discount
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item


# ──────────────── UPDATE QUANTITY ────────────────

@sales_router.put("/update/{cart_item_id}", response_model=CartResponse)
def update_cart_item(cart_item_id: int, cart_data: CartUpdate, db: Session = Depends(get_db)):

    cart_item = db.query(Cart).filter(Cart.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Utilise Furniture au lieu de Product
    product = db.query(Furniture).filter(
        Furniture.ProductID == cart_item.product_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if cart_data.quantity is not None:
        if cart_data.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
        cart_item.quantity = cart_data.quantity
        cart_item.subtotal = cart_item.quantity * product.price

    if cart_data.discount is not None:
        cart_item.discount = cart_data.discount

    db.commit()
    db.refresh(cart_item)
    return cart_item


# ──────────────── REMOVE ONE ITEM ────────────────

@sales_router.delete("/remove/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db)):

    cart_item = db.query(Cart).filter(Cart.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart successfully"}


# ──────────────── CLEAR ENTIRE CART ────────────────

@sales_router.delete("/clear/{customer_id}")
def clear_cart(customer_id: int, db: Session = Depends(get_db)):

    cart_items = db.query(Cart).filter(Cart.customer_id == customer_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is already empty")

    db.query(Cart).filter(Cart.customer_id == customer_id).delete()
    db.commit()
    return {"message": "Cart cleared successfully"}



# @sales_router.post('/create_order{id_cart}')



# ──────────────── GET CART BY CUSTOMER ────────────────

@sales_router.get("/{customer_id}", response_model=List[CartResponse])
def get_cart(customer_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.customer_id == customer_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    return cart_items


# ──────────────── ADD TO CART ────────────────

@sales_router.post("/add", response_model=CartResponse)
def add_to_cart(cart_data: CartCreate, db: Session = Depends(get_db)):
    product = db.query(Furniture).filter(Furniture.ProductID == cart_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(Cart).filter(
        Cart.customer_id == cart_data.customer_id,
        Cart.product_id  == cart_data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += cart_data.quantity
        existing_item.subtotal  = existing_item.quantity * product.price
        db.commit()
        db.refresh(existing_item)
        return existing_item

    subtotal = cart_data.quantity * product.price
    new_item = Cart(
        product_id  = cart_data.product_id,
        customer_id = cart_data.customer_id,
        quantity    = cart_data.quantity,
        subtotal    = subtotal,
        discount    = cart_data.discount
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# ──────────────── UPDATE QUANTITY ────────────────

@sales_router.put("/update/{cart_item_id}", response_model=CartResponse)
def update_cart_item(cart_item_id: int, cart_data: CartUpdate, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    product = db.query(Furniture).filter(Furniture.ProductID == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if cart_data.quantity is not None:
        if cart_data.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
        cart_item.quantity = cart_data.quantity
        cart_item.subtotal = cart_item.quantity * product.price

    if cart_data.discount is not None:
        cart_item.discount = cart_data.discount

    db.commit()
    db.refresh(cart_item)
    return cart_item


# ──────────────── REMOVE ONE ITEM ────────────────

@sales_router.delete("/remove/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart successfully"}


# ──────────────── CLEAR ENTIRE CART ────────────────

@sales_router.delete("/clear/{customer_id}")
def clear_cart(customer_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.customer_id == customer_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is already empty")
    db.query(Cart).filter(Cart.customer_id == customer_id).delete()
    db.commit()
    return {"message": "Cart cleared successfully"}


# ──────────────── CREATE ORDER FROM CART + PROCESS PAYMENT ────────────────

@sales_router.post("/create_order/{customer_id}", response_model=OrderSummaryResponse)
def create_order(
    customer_id: int,
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    # 1. Load cart items
    cart_items = db.query(Cart).filter(Cart.customer_id == customer_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    # 2. Create one Order row per cart item
    order_ids   = []
    total_price = 0.0

    for item in cart_items:
        product = db.query(Furniture).filter(Furniture.ProductID == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        final_price = item.subtotal - item.discount
        total_price += final_price

        order = Order(
            product_id   = item.product_id,
            customer_id  = customer_id,
            status       = "pending",
            totalprice   = final_price,
            product_qte  = item.quantity,
        )
        db.add(order)
        db.flush()          # get order.id before commit
        order_ids.append(order.id)

    # 3. Create Payment linked to the first order
    #    (one payment covers the whole checkout session)
    payment = Payment(
        order_id    = order_ids[0],
        customer_id = customer_id,
        amount      = total_price,
        method      = payment_data.method,
        status      = PaymentStatus.completed,   # simulate success
        card_last4  = payment_data.card_number[-4:],
        cardholder  = payment_data.cardholder,
    )
    db.add(payment)

    # 4. Clear the cart
    db.query(Cart).filter(Cart.customer_id == customer_id).delete()

    db.commit()
    db.refresh(payment)

    return OrderSummaryResponse(
        order_ids   = order_ids,
        total_price = total_price,
        payment     = PaymentResponse.model_validate(payment),
    )

STATUS_FLOW = ["pending", "confirmed", "preparing", "shipped", "delivering", "delivered"]



# ──────────────── GET ALL ORDERS FOR CUSTOMER ────────────────

@sales_router.get("/get_orders/{customer_id}", response_model=OrderTrackingResponse)
def get_orders(customer_id: int, db: Session = Depends(get_db)):
    orders = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    # Attach product info manually (eager load)
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
            product     = ProductInfo.model_validate(product) if product else None,
        ))

    total_price = sum(o.totalprice for o in orders)

    # Get latest payment for this customer
    payment = (
        db.query(Payment)
        .filter(Payment.customer_id == customer_id)
        .order_by(Payment.created_at.desc())
        .first()
    )

    return OrderTrackingResponse(
        orders      = order_details,
        total_price = total_price,
        payment     = PaymentInfo.model_validate(payment) if payment else None,
    )


# ──────────────── UPDATE ORDER STATUS ────────────────

@sales_router.put("/{order_id}/status")
def update_order_status(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_index = STATUS_FLOW.index(order.status) if order.status in STATUS_FLOW else 0
    if current_index < len(STATUS_FLOW) - 1:
        order.status = STATUS_FLOW[current_index + 1]
        db.commit()
        db.refresh(order)

    return {"order_id": order.id, "new_status": order.status}


# ──────────────── CANCEL ORDER ────────────────

@sales_router.put("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status in ["shipped", "delivering", "delivered"]:
        raise HTTPException(status_code=400, detail=f"Cannot cancel order with status '{order.status}'")

    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return {"order_id": order.id, "status": "cancelled"}



