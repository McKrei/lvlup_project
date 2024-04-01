from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, condecimal, validator
from enum import Enum


class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioOut(PortfolioBase):
    id: int
    user_id: int
