from fastapi import APIRouter, Depends, status, Form
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_session
from database.models import Portfolio, User
from .schemas import PortfolioCreate, PortfolioOut
from .crud import CRUDPortfolio
from user.dependency import get_current_user


router = APIRouter(prefix="/portfolio", tags=["portfolio"])



@router.post("/", response_model=PortfolioOut, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio: PortfolioCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    data = {**portfolio.model_dump(), "user_id": user.id}
    portfolio = await CRUDPortfolio.create(session, data)
    if not portfolio:
        raise HTTPException(status_code=400, detail="Asset could not be created")
    return portfolio


@router.get("/", response_model=list[PortfolioOut])
async def get_portfolio(
    session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)
):
    return await CRUDPortfolio.get_all_by_user_id(session, user.id)


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(
    portfolio_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    portfolio = await CRUDPortfolio.get_by_id(session, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="portfolio not found")
    if portfolio.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await CRUDPortfolio.delete(session, portfolio)
    return


@router.put("/{portfolio_id}", response_model=PortfolioOut)
async def update_portfolio(
    portfolio_id: int,
    asset: PortfolioCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
):
    asset = await CRUDPortfolio.get_by_id(session, portfolio_id)
    if not asset:
        raise HTTPException(status_code=404, detail="portfolio not found")
    updated_asset = await CRUDPortfolio.update(
        session, portfolio_id, asset.model_dump()
    )
    if not updated_asset:
        raise HTTPException(status_code=404, detail="portfolio not found")
    return updated_asset
