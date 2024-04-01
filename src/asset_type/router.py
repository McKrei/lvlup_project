from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from database.models import User
from .schemas import AssetTypeCreate, AssetTypeOut
from .crud import CRUDAssetType
from user.dependency import get_current_user


router = APIRouter(prefix="/asset_types", tags=["asset_types"])


@router.post("/", response_model=AssetTypeOut, status_code=status.HTTP_201_CREATED)
async def create_asset_type(
    asset_type: AssetTypeCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = {**asset_type.model_dump(), "user_id": user.id}
    new_asset_type = await CRUDAssetType.create(session, data)
    if not new_asset_type:
        raise HTTPException(status_code=400, detail="AssetType could not be created")
    return new_asset_type


@router.get("/", response_model=list[AssetTypeOut])
async def get_asset_types(
    session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)
):
    asset_types = await CRUDAssetType.get_all_by_user_id(session, user.id)
    return asset_types


@router.delete("/{asset_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset_type(
    asset_type_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    asset_type = await CRUDAssetType.get_by_id(session, asset_type_id)
    if not asset_type:
        raise HTTPException(status_code=404, detail="AssetType not found")
    if asset_type.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await CRUDAssetType.delete(session, asset_type)
    return
