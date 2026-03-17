
import os
import pickle
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

import tensorflow as tf
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sklearn.preprocessing import MinMaxScaler

from app.core.database import get_db
from app.models.Sale import Sale
from app.api.auth import get_current_user
from app.schemas.Prediction import NextMonthPrediction
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = os.getenv("HF_TOKEN")


# ── Artifact paths ────────────────────────────────────────────────────────────
ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../model")
MODEL_PATH    = os.path.join(ARTIFACTS_DIR, "sales_predictor.keras")
SCALER_PATH   = os.path.join(ARTIFACTS_DIR, "new_scaler.pkl")

WINDOW = 12   # matches notebook window=12

prediction_router = APIRouter(prefix="/api/prediction", tags=["prediction"])

_model  = None
_scaler = None


def _load():
    global _model, _scaler

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(status_code=500, detail=f"Model not found: {MODEL_PATH}")
        _model = tf.keras.models.load_model(MODEL_PATH)

    if _scaler is None:
        if not os.path.exists(SCALER_PATH):
            raise HTTPException(
                status_code=500,
                detail=(
                    "scaler.pkl not found. "
                    "Add this to your notebook and run it:\n\n"
                    "import pickle\n"
                    "with open('scaler.pkl', 'wb') as f:\n"
                    "    pickle.dump(sales_scaled, f)"
                )
            )
        with open(SCALER_PATH, "rb") as f:
            _scaler = pickle.load(f)

    return _model, _scaler








@prediction_router.get("/next-month", response_model=NextMonthPrediction)
def predict_next_month(
    db:   Session = Depends(get_db),
    # user          = Depends(get_current_user),
):
    model, scaler = _load()

    # ── 1. Fetch Sales from DB ────────────────────────────────────────────────
    rows = (
        db.query(Sale.order_date, Sale.sales)
        .order_by(Sale.order_date.asc())
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="No sales data found.")

    # ── 2. Resample to monthly — mirrors cell 14 ──────────────────────────────
    # monthly_sales = df['Sales'].resample('ME').sum()
    df = pd.DataFrame(rows, columns=["order_date", "sales"])
    df["order_date"] = pd.to_datetime(df["order_date"])
    df = df.set_index("order_date")
    monthly_sales = df["sales"].resample("ME").sum()

    if len(monthly_sales) < WINDOW:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least {WINDOW} months of data. Only have {len(monthly_sales)}."
        )

    # ── 3. Scale — mirrors cell 17 ────────────────────────────────────────────
    # sales_scaled.fit_transform(monthly_sales.values.reshape(-1,1))
    # We use transform() because scaler is already fitted from the notebook
    monthly_values   = monthly_sales.values.reshape(-1, 1).astype("float32")
    monthly_scaled   = scaler.transform(monthly_values)  # shape (n_months, 1)

    # ── 4. Build input window — mirrors cell 18 ───────────────────────────────
    # X[-1] reshaped to (1, 12, 1)
    X_window = monthly_scaled[-WINDOW:].reshape(1, WINDOW, 1)

    # ── 5. Predict — mirrors cell 26 ──────────────────────────────────────────
    # y_pred = model.predict(X_test)
    y_pred = model.predict(X_window, verbose=0)           # shape (1, 1)

    # ── 6. Inverse transform — mirrors cell 27 ────────────────────────────────
    # sales_scaled.inverse_transform(y_pred)
    pred_real = float(scaler.inverse_transform(y_pred)[0][0])
    pred_real = max(pred_real, 0.0)

    # ── 7. Response ───────────────────────────────────────────────────────────
    last_date  = monthly_sales.index[-1]
    last_sales = float(monthly_sales.iloc[-1])
    next_date  = last_date + relativedelta(months=1)
    change_pct = ((pred_real - last_sales) / last_sales * 100) if last_sales > 0 else 0.0

    return NextMonthPrediction(
        last_month       = last_date.strftime("%Y-%m"),
        last_month_sales = round(last_sales, 2),
        next_month       = next_date.strftime("%Y-%m"),
        predicted_sales  = round(pred_real, 2),
        change_pct       = round(change_pct, 2),
        r2_score         = 0.6337,
    )