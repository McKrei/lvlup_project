from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Asset
from database.crud_base import CRUDBaseByUser



class CRUDAsset(CRUDBaseByUser):
    model = Asset
