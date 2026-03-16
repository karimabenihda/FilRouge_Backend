from pydantic import BaseModel

class DashboardStats(BaseModel):
    total_revenue:  float
    total_profit:   float
    total_orders:   int
    pending_orders: int

class MonthlyChartItem(BaseModel):
    date:    str   
    revenue: float
    profit:  float