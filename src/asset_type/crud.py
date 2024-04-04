from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from database.models import AssetType
from database.crud_base import CRUDBaseByUser


class CRUDAssetType(CRUDBaseByUser):
    model = AssetType

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
        cls, session: AsyncSession, name: str, user_id: int
    ) -> tuple[bool, model]:
        is_created = False
        portfolio = await cls.get_by_name_and_user_id(session, name, user_id)
        if not portfolio:
            is_created = True
            data = {"name": name, "user_id": user_id}
            portfolio = await cls.create(session, data)
        return is_created, portfolio
