from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas.User import Token
from api.auth import router
from core.database import  Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router,prefix="/api/auth")
 