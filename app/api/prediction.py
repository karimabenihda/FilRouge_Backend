
import os
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

import tensorflow as tf
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.core.database import get_db
from app.models.Sale import Sale
from app.api.auth import get_current_user
from app.schemas.Prediction import NextMonthPrediction ,p
# ── Path to model artifacts ───────────────────────────────────────────────────
ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
MODEL_PATH    = os.path.join(ARTIFACTS_DIR, "sales_predictor.keras")
SCALER_PATH   = os.path.join(ARTIFACTS_DIR, "scaler.pkl")

WINDOW = 12   # must match training (notebook used window=12)

prediction_router = APIRouter(prefix="/api/prediction", tags=["prediction"])
# ── Lazy singletons — loaded once on first request ────────────────────────────
_model  = None
_scaler = None


def _load():
    global _model, _scaler

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=500,
                detail=f"Model not found at {MODEL_PATH}. Make sure sales_predictor.keras is in the project root."
            )
        _model = tf.keras.models.load_model(MODEL_PATH)

    if _scaler is None:
        if not os.path.exists(SCALER_PATH):
            raise HTTPException(
                status_code=500,
                detail="scaler.pkl not found. Run save_scaler_from_db.py first to generate it."
            )
        with open(SCALER_PATH, "rb") as f:
            _scaler = pickle.load(f)

    return _model, _scaler


# ── Router ────────────────────────────────────────────────────────────────────


# ── Schema ────────────────────────────────────────────────────────────────────

# ── GET /api/prediction/next-month ───────────────────────────────────────────
@prediction_router.get("/next-month", response_model=NextMonthPrediction)
def predict_next_month(
    db:   Session = Depends(get_db),
    user          = Depends(get_current_user),
):

    model, scaler = _load()

    # ── 1. Fetch + resample monthly sales from DB ─────────────────────────────
    rows = (
        db.query(Sale.order_date, Sale.sales)
        .order_by(Sale.order_date.asc())
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="No sales data in the database.")

    df = pd.DataFrame(rows, columns=["order_date", "sales"])
    df["order_date"] = pd.to_datetime(df["order_date"])
    df = df.set_index("order_date")

    # mirrors: df['Sales'].resample('ME').sum()
    monthly = df["sales"].resample("ME").sum()

    if len(monthly) < WINDOW:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least {WINDOW} months of data to predict. Only have {len(monthly)}."
        )

    # ── 2. Scale ──────────────────────────────────────────────────────────────
    monthly_values = monthly.values.reshape(-1, 1).astype("float32")
    scaled         = scaler.transform(monthly_values)

    # ── 3. Build input window — last 12 months ────────────────────────────────
    window = scaled[-WINDOW:].reshape(1, WINDOW, 1)   # shape (1, 12, 1)

    # ── 4. Predict ────────────────────────────────────────────────────────────
    pred_scaled = model.predict(window, verbose=0)     # shape (1, 1)

    # ── 5. Inverse transform → real dollars ──────────────────────────────────
    pred_real = scaler.inverse_transform(pred_scaled)[0][0]
    pred_real = max(float(pred_real), 0.0)             # no negative sales

    # ── Build response ────────────────────────────────────────────────────────
    last_date        = monthly.index[-1]
    last_sales       = float(monthly.iloc[-1])
    next_month_date  = last_date + relativedelta(months=1)

    change_pct = (
        ((pred_real - last_sales) / last_sales) * 100
        if last_sales > 0 else 0.0
    )

    return NextMonthPrediction(
        last_month       = last_date.strftime("%Y-%m"),
        last_month_sales = round(last_sales, 2),
        next_month       = next_month_date.strftime("%Y-%m"),
        predicted_sales  = round(pred_real, 2),
        change_pct       = round(change_pct, 2),
        r2_score         = 0.6337,
    )




# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime
# from app.core.database import get_db
# from app.schemas.Prediction import SalesPrediction,RecommandationInput
# import joblib
# import os
# import pandas as pd

# prediction_router = APIRouter()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SALES_MODEL_PATH = os.path.join(BASE_DIR, "sales_predictor.joblib")

# RECOMMENDATION_MODEL_PATH = os.path.join(BASE_DIR, "recommendation_system.joblib")

# sales_model = joblib.load(SALES_MODEL_PATH)
# recommendation_model = joblib.load(RECOMMENDATION_MODEL_PATH)

# @prediction_router.post('/predict_sales')
# def sales_prediction(data:SalesPrediction):
#     df = pd.DataFrame([data.dict()])
#     prediction =sales_model.predict(df)
#     return {"expected_sales": prediction}


# @prediction_router.post('/recommend_furnitures')
# def furniture_recommendation(data:RecommandationInput):
#     df = pd.DataFrame([data.dict()])
#     prediction =recommendation_model.predict(df)
#     return {"expected_sales": prediction}

