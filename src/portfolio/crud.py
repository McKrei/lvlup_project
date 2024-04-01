from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Portfolio
from fastapi import HTTPException

from database.crud_base import CRUDBaseByUser


class CRUDPortfolio(CRUDBaseByUser):
    model = Portfolio

