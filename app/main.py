from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.auth import router
from core.database import  Base, engine
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

app.include_router(router,prefix="/api/auth")
 