from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import AssetType
from database.crud_base import CRUDBaseByUser



class CRUDAssetType(CRUDBaseByUser):
    model = AssetType
