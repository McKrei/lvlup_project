from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .database import Base


class CRUDBase:
    model: Base = Base

    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> model | None:
        """Создание нового объект."""
        try:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
        except IntegrityError:
            await session.rollback()
            return None

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[model]:
        """Получение всех объектов."""
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> model | None:
        """Получение объект по ID."""
        query = select(cls.model).filter(cls.model.id == id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @classmethod
    async def update(
        cls, session: AsyncSession, obj: model, update_data: dict
    ) -> model | None:
        """Обновление данных объекта."""
        try:
            for key, value in update_data.items():
                setattr(obj, key, value)
            await session.commit()
            return obj
        except IntegrityError:
            await session.rollback()
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, obj: model):
        """Удаление объекта."""
        await session.delete(obj)
        await session.commit()


class CRUDBaseByUser(CRUDBase):
    model: Base = Base

    @classmethod
    async def get_all_by_user_id(cls, session: AsyncSession, user_id: int) -> list[model]:
        """Получение всех объектов по ID пользователя."""
        query = select(cls.model).filter(cls.model.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()
