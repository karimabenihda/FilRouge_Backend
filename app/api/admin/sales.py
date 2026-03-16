from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.core.database import get_db
from app.models.Sale import Sale
from app.api.auth import get_current_user
from typing import List
from pydantic import BaseModel
from app.schemas.Sale import MonthlySalesItem ,YearlySalesItem


sales_analytics_router = APIRouter(prefix="/api/analytics", tags=["analytics"])






# ─── GET /api/analytics/sales/monthly ────────────────────────────────────────
# Flat list — every (year, month) bucket sorted oldest → newest
# Example: [{ year: 2014, month: 1, total_sales: 3200.5, ... }, ...]

@sales_analytics_router.get("/sales/monthly", response_model=List[MonthlySalesItem])
def get_monthly_sales(
    db:   Session = Depends(get_db),
    user          = Depends(get_current_user),
):
    rows = (
        db.query(
            extract("year",  Sale.order_date).label("year"),
            extract("month", Sale.order_date).label("month"),
            func.round(func.sum(Sale.sales).cast(type_=__import__('sqlalchemy').Numeric), 2).label("total_sales"),
            func.round(func.sum(Sale.profit).cast(type_=__import__('sqlalchemy').Numeric), 2).label("total_profit"),
            func.count(Sale.row_id).label("total_orders"),
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
        MonthlySalesItem(
            year         = int(r.year),
            month        = int(r.month),
            total_sales  = float(r.total_sales  or 0),
            total_profit = float(r.total_profit or 0),
            total_orders = r.total_orders,
        )
        for r in rows
    ]


# ─── GET /api/analytics/sales/yearly ─────────────────────────────────────────
# Grouped by year, with each year containing its monthly breakdown
# Example: [{ year: 2014, total_sales: 45000, months: [...] }, ...]

@sales_analytics_router.get("/sales/yearly", response_model=List[YearlySalesItem])
def get_yearly_sales(
    db:   Session = Depends(get_db),
    user          = Depends(get_current_user),
):
    rows = (
        db.query(
            extract("year",  Sale.order_date).label("year"),
            extract("month", Sale.order_date).label("month"),
            func.sum(Sale.sales).label("total_sales"),
            func.sum(Sale.profit).label("total_profit"),
            func.count(Sale.row_id).label("total_orders"),
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

    # Group months under each year
    year_map = {}
    for r in rows:
        year = int(r.year)
        month_item = MonthlySalesItem(
            year         = year,
            month        = int(r.month),
            total_sales  = round(float(r.total_sales  or 0), 2),
            total_profit = round(float(r.total_profit or 0), 2),
            total_orders = r.total_orders,
        )
        if year not in year_map:
            year_map[year] = {
                "year":         year,
                "total_sales":  0.0,
                "total_profit": 0.0,
                "total_orders": 0,
                "months":       [],
            }
        year_map[year]["total_sales"]  += month_item.total_sales
        year_map[year]["total_profit"] += month_item.total_profit
        year_map[year]["total_orders"] += month_item.total_orders
        year_map[year]["months"].append(month_item)

    return [
        YearlySalesItem(
            year         = v["year"],
            total_sales  = round(v["total_sales"],  2),
            total_profit = round(v["total_profit"], 2),
            total_orders = v["total_orders"],
            months       = v["months"],
        )
        for v in sorted(year_map.values(), key=lambda x: x["year"])
    ]