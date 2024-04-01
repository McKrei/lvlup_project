# src/transaction/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from .schemas import TransactionCreate, TransactionOut
from .crud import CRUDTransaction
from user.dependency import get_current_user
from database.models import User


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    new_transaction = await CRUDTransaction.create(
        session, transaction_data.model_dump()
    )
    return new_transaction


@router.get("/", response_model=list[TransactionOut])
async def get_transactions_by_asset_id(
    asset_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    transactions = await CRUDTransaction.get_all_by_asset_id(session, asset_id)
    return transactions


@router.get("/", response_model=list[TransactionOut])
async def get_transactions_by_user_id(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    transactions = await CRUDTransaction.get_all_by_user_id(session, user.id)
    return transactions


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    await CRUDTransaction.delete(session, transaction_id)
    return
