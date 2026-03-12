from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas.User import Token
# from app.api.auth import router
from app.api.auth import auth_router
from app.api.furnitures import furnitures_router
from app.api.sales import sales_router
from app.models.Inventory import InventoryLog
from app.models.Prediction import Recommendation, SalesPrediction
from app.core.database import Base, engine
from app.api.inventory import inventory_router
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(furnitures_router, prefix="/api/furnitures", tags=["furnitures"])
app.include_router(sales_router, prefix="/api/sales", tags=["sales"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["inventory"])
