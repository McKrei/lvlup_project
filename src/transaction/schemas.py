from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, condecimal, validator
from enum import Enum


class TransactionType(str, Enum):
    Buy = "Buy"
    Sell = "Sell"
    Dividend = "Dividend"


class TransactionBase(BaseModel):
    type: TransactionType
    quantity: condecimal(gt=0)
    price: condecimal(gt=0)
    asset_id: int


class TransactionCreate(TransactionBase):
    pass



class TransactionOut(TransactionBase):
    id: int
    created_at: datetime
