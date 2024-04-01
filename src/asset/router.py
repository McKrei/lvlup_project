from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from database.models import Asset, User
from .schemas import AssetCreate, AssetOut
from .crud import CRUDAsset
from user.dependency import get_current_user


router = APIRouter(prefix="/asset", tags=["asset"])


@router.post("/", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset: AssetCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    new_asset = await CRUDAsset.create(session, asset.model_dump())
    if not new_asset:
        raise HTTPException(status_code=400, detail="Asset could not be created")
    return new_asset


@router.get("/", response_model=list[AssetOut])
async def get_assets(
    session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)
):
    assets = await CRUDAsset.get_all_by_user_id(session, user.id)
    return assets


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    asset = await CRUDAsset.get_by_id(session, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await CRUDAsset.delete(session, asset)
    return


@router.put("/{asset_id}", response_model=AssetOut)
async def update_asset(
    asset_id: int,
    asset: AssetCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    asset = await CRUDAsset.get_by_id(session, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    updated_asset = await CRUDAsset.update(session, asset_id, asset.model_dump())
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return updated_asset
