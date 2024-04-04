from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database.models import Asset, AssetType, Portfolio, User
from database.crud_base import CRUDBaseByUser


class CRUDAsset(CRUDBaseByUser):
    model = Asset

    @classmethod
    async def get_all_by_user_id_or_portfolio_id(
        cls, session: AsyncSession, user_id: int, portfolio_id: int = None
    ) -> list:
        query = (
            select(cls.model)
            .options(joinedload(cls.model.portfolio), joinedload(cls.model.asset_type))
            .filter(Portfolio.user_id == user_id)
            .distinct()
        )

        if portfolio_id:
            query = query.filter(cls.model.portfolio_id == portfolio_id)

        result = await session.execute(query)
        assets = result.scalars().all()

        return [
            {
                "id": asset.id,
                "asset_name": asset.name,
                "quantity": asset.quantity,
                "purchase_price": asset.purchase_price,
                "current_price": asset.current_price,
                "commission": asset.commission,
                "portfolio_name": asset.portfolio.name if asset.portfolio else None,
                "asset_type": asset.asset_type.name if asset.asset_type else None,
                "price_one": (
                    round(asset.current_price / asset.quantity, 2)
                    if asset.quantity and asset.current_price
                    else 0
                ),
            }
            for asset in assets
        ]
