from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.api.auth import auth_router
from app.api.sales import sales_router
from app.core.database import  Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

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

app.include_router(auth_router,prefix="/api/auth", tags=["Auth"])
app.include_router(sales_router,prefix="/api/sales", tags=["Sales"])
 