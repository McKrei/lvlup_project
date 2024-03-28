from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import create_all, drop_all, get_session
from database.models import User
from user.router import router as user_router


app = FastAPI()

app.include_router(user_router)


@app.get("/update_table")
async def update_table():
    await drop_all()
    await create_all()
    return 200
