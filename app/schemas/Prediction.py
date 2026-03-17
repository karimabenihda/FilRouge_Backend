from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional

class NextMonthPrediction(BaseModel):
    last_month:       str    # "YYYY-MM" — last month in the data
    last_month_sales: float  # actual sales of that month
    next_month:       str    # "YYYY-MM" — the month being predicted
    predicted_sales:  float  # LSTM prediction in real dollars
    change_pct:       float  # % change vs last known month
    r2_score:         float  # model accuracy from notebook: 0.6337
    # suggestion_plan: Optional[str] = None



class SalesPrediction(BaseModel):
    City: str
    Region: str
    Category: str
    SubCategory: str

    Quantity: int
    Discount: float
    Profit: float

    # brand one-hot
    brand_Ashley_Furniture: int
    brand_IKEA: int
    brand_La_Z_Boy: int
    brand_West_Elm: int

    # season one-hot
    season_Fall: int
    season_Spring: int
    season_Summer: int
    season_Winter: int

    # segment one-hot
    Segment_Consumer: int
    Segment_Corporate: int
    Segment_Home_Office: int

    # ship mode one-hot
    ShipMode_First_Class: int
    ShipMode_Same_Day: int
    ShipMode_Second_Class: int
    ShipMode_Standard_Class: int



class SalesPrediction(BaseModel):
    month: datetime
    expected_sales: float
    threshold: float
    risk_level: float
    plans: List[str] 

class SalesPredictionHistory(BaseModel):
    month: datetime
    expected_sales: float
    real_sales:float
    threshold: float
    risk_level: float
    plans: List[str] 

class RecommandationInput(BaseModel):
    CustomerID: str
    ProductID: str
    Ship_Mode :int
    Segment :int
    City :int
    Region :int
    Category :int
    Sub_Category :int
    Quantity :int
    season :int
    brand:int

class RecommendationRequest(BaseModel):
    CustomerID: str
    top_n: int = 5

class Recommandation(BaseModel):
    CustomerID: str
    recommended_products: List[str]