from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Transaction
from fastapi import HTTPException

from database.crud_base import CRUDBaseByUser


class CRUDTransaction(CRUDBaseByUser):
    model = Transaction

    @classmethod
    async def get_all_by_asset_id(cls, session: AsyncSession, asset_id: int) -> list[model]:
        query = select(cls.model).filter(cls.model.asset_id == asset_id)
        result = await session.execute(query)
        transactions = result.scalars().all()
        return transactions
