from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.schemas.User import Token
# from app.api.auth import router
from app.api.auth import auth_router
from app.api.furnitures import furnitures_router
from app.api.sales import sales_router

app = FastAPI()
# models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth_router,prefix="/api/auth",tags='auth')
app.include_router(furnitures_router,prefix="/api/furnitures", tags='furnitures')
app.include_router(sales_router,prefix="/api/sales" ,tags='sales')