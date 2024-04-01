from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database.database import create_tables
from user.router import router as user_router
from asset_type.router import router as asset_type_router
from asset.router import router as asset_router
from portfolio.router import router as portfolio_router
from transaction.router import router as transaction_router
from ip_weather.router import router as ip_weather_router
from frontend.router import router as frontend_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    # await create_tables()
    yield
    print("Приложение останавливается...")


app = FastAPI(lifespan=lifespan)
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

app.include_router(user_router)
app.include_router(asset_type_router)
app.include_router(asset_router)
app.include_router(portfolio_router)
app.include_router(transaction_router)
app.include_router(ip_weather_router)
app.include_router(frontend_router)



@app.on_event("startup")
async def startup_event():
    print("Приложение запускается 2...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Приложение останавливается 2...")
