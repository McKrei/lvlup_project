from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, condecimal, validator



class AssetBase(BaseModel):
    name: str
    quantity: condecimal(gt=0)
    purchase_price: condecimal(gt=0)
    current_price: condecimal(gt=0)
    commission: condecimal(ge=0)
    portfolio_id: int
    asset_type_id: int

class AssetUpdate(AssetBase):
    pass


class AssetCreate(AssetBase):
    pass

class AssetOut(AssetBase):
    id: int
    portfolio_id: int
    asset_type_id: int
