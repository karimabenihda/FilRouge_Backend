from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.schemas.User import Token
from app.api.auth import router

app = FastAPI()
# models.Base.metadata.create_all(bind=database.engine)

app.include_router(router,prefix="/api/auth")
 