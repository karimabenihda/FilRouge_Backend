from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.core.database import get_db
from app.models.Sale import Order, Sale
from app.api.auth import get_current_user
from pydantic import BaseModel
from typing import List
from app.schemas.Dashboard import DashboardStats, MonthlyChartItem

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])



# ─── GET /api/dashboard/stats ─────────────────────────────────────────────────
# Powers the 4 SectionCards

@dashboard_router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db:   Session = Depends(get_db),
    user          = Depends(get_current_user),
):
    revenue, profit = db.query(
        func.coalesce(func.sum(Sale.sales),  0),
        func.coalesce(func.sum(Sale.profit), 0),
    ).first()

    total_orders   = db.query(func.count(Order.id)).scalar()
    pending_orders = db.query(func.count(Order.id)).filter(Order.status == "pending").scalar()

    return DashboardStats(
        total_revenue  = round(float(revenue), 2),
        total_profit   = round(float(profit),  2),
        total_orders   = total_orders,
        pending_orders = pending_orders,
    )


# ─── GET /api/dashboard/chart ─────────────────────────────────────────────────
# Powers ChartAreaInteractive — monthly revenue + profit from the sales table

@dashboard_router.get("/chart", response_model=List[MonthlyChartItem])
def get_dashboard_chart(
    db:   Session = Depends(get_db),
    user          = Depends(get_current_user),
):
    rows = (
        db.query(
            extract("year",  Sale.order_date).label("year"),
            extract("month", Sale.order_date).label("month"),
            func.sum(Sale.sales).label("revenue"),
            func.sum(Sale.profit).label("profit"),
        )
        .group_by(
            extract("year",  Sale.order_date),
            extract("month", Sale.order_date),
        )
        .order_by(
            extract("year",  Sale.order_date),
            extract("month", Sale.order_date),
        )
        .all()
    )

    return [
        MonthlyChartItem(
            date    = f"{int(r.year)}-{int(r.month):02d}-01",
            revenue = round(float(r.revenue or 0), 2),
            profit  = round(float(r.profit  or 0), 2),
        )
        for r in rows
    ]