from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Portfolio
from fastapi import HTTPException

from database.crud_base import CRUDBaseByUser


class CRUDPortfolio(CRUDBaseByUser):
    model = Portfolio

    @classmethod
    async def get_by_name_and_user_id(
        cls, session: AsyncSession, name: str, user_id: int
    ) -> model | None:
        """Получение объекта по имени."""
        query = select(cls.model).filter(cls.model.name == name, user_id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_or_create(
        cls, session: AsyncSession, name: str, user_id: int, description: str = ""
    ) -> tuple[bool, model]:
        """
        Получение или создание Портфеля.
        Возвращает кортеж из двух значений:
        1. Флаг создания нового объекта.
        2. Объект Портфеля.
        """
        is_created = False
        portfolio = await cls.get_by_name_and_user_id(session, name, user_id)
        if not portfolio:
            is_created = True
            data = {"name": name, "user_id": user_id, "description": description}
            portfolio = await cls.create(session, data)
        return is_created, portfolio
