from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, condecimal, validator
from enum import Enum


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]


class UserOut(UserBase):
    id: int
