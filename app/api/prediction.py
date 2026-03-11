from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.schemas.Prediction import SalesPrediction,RecommandationInput
import joblib
import os
import pandas as pd

prediction_router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SALES_MODEL_PATH = os.path.join(BASE_DIR, "sales_predictor.joblib")

RECOMMENDATION_MODEL_PATH = os.path.join(BASE_DIR, "recommendation_system.joblib")

sales_model = joblib.load(SALES_MODEL_PATH)
recommendation_model = joblib.load(RECOMMENDATION_MODEL_PATH)

@prediction_router.post('/predict_sales')
def sales_prediction(data:SalesPrediction):
    df = pd.DataFrame([data.dict()])
    prediction =sales_model.predict(df)
    return {"expected_sales": prediction}


@prediction_router.post('/recommend_furnitures')
def furniture_recommendation(data:RecommandationInput):
    df = pd.DataFrame([data.dict()])
    prediction =recommendation_model.predict(df)
    return {"expected_sales": prediction}

