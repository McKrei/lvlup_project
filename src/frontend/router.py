from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from user.dependency import get_correct_user_frontend, get_current_user
from database.models import User
from database.database import get_session
from .dependency import get_user_or_redirect
from portfolio.crud import CRUDPortfolio
from asset_type.crud import CRUDAssetType
from asset.crud import CRUDAsset
from asset.schemas import AssetUpdate


router = APIRouter(prefix="", tags=["frontend"])

templates = Jinja2Templates(directory="frontend/template")


@router.get("/auth")
async def get_login(
    request: Request,
    user: User | None = Depends(get_correct_user_frontend),
    not_auth: bool | None = None,
):
    # if user:
    #     return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    return templates.TemplateResponse(
        "auth.html", {"request": request, "not_auth": not_auth}
    )


@router.get("/logout", response_class=RedirectResponse)
async def get_logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/register")
async def get_register(
    request: Request, user: User | None = Depends(get_correct_user_frontend)
):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/portfolio")
async def get_portfolio(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    data = await CRUDPortfolio.get_all_by_user_id(session, user.id)

    return templates.TemplateResponse(
        "page/portfolio.html", {"request": request, "user": user, "data": data}
    )


@router.post("/portfolio")
async def add_portfolio(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    name: str = Form(...),
    description: str | None = Form(None),
    session: AsyncSession = Depends(get_session),
):
    # Проверка на уникальность имени портфеля
    portfolio = await CRUDPortfolio.get_by_name_and_user_id(session, name, user.id)
    if portfolio:
        url = "/portfolio"
        request.session["message"] = "Портфель с таким именем уже существует"

    else:
        data = {"name": name, "description": description, "user_id": user.id}
        portfolio = await CRUDPortfolio.create(session, data)
        url += f"asset?portfolio_id={portfolio.id}"

    return RedirectResponse(url=url, status_code=301)


@router.get("/asset")
async def get_asset(
    request: Request,
    portfolio_id: int | None = None,
    user: User = Depends(get_user_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    data = await CRUDAsset.get_all_by_user_id_or_portfolio_id(session, user.id, portfolio_id)
    data = {
        "assets": data,
        "portfolio_names": set(asset["portfolio_name"] for asset in data),
        "asset_types": set(asset["asset_type"] for asset in data),
    }
    return templates.TemplateResponse(
        "page/asset.html", {"request": request, "user": user, "data": data}
    )


@router.post("/asset")
async def add_asset(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    name: str = Form(...),
    purchase_price: float = Form(...),
    current_price: float = Form(...),
    commission: float = Form(0),
    portfolio_name: str = Form(...),
    asset_type_name: str = Form(...),
    quantity: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    # Проверка на уникальность имени портфеля
    _, portfolio = await CRUDPortfolio.get_or_create(session, portfolio_name, user.id)
    _, asset_type = await CRUDAssetType.get_or_create(session, asset_type_name, user.id)

    data = {
        "name": name,
        "purchase_price": purchase_price,
        "current_price": current_price,
        "commission": commission,
        "portfolio_id": portfolio.id,
        "asset_type_id": asset_type.id,
        "quantity": quantity,
    }
    asset = await CRUDAsset.create(session, data)
    return RedirectResponse(url="/asset", status_code=301)


@router.post("/update-asset-price")
async def update_asset_price(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    current_price_per_unit: float = Form(...),
    quantity: float = Form(...),
    asset_id: int = Form(...),
    session: AsyncSession = Depends(get_session),
):
    new_current_price = current_price_per_unit * quantity
    data = {"current_price": new_current_price, "quantity": quantity}
    asset = await CRUDAsset.get_by_id(session, asset_id)
    await CRUDAsset.update(session, asset, data)
    return RedirectResponse(url="/asset", status_code=301)


@router.get("/transaction")
async def get_transaction(request: Request, user: User = Depends(get_user_or_redirect)):
    data = None
    return templates.TemplateResponse(
        "page/transaction.html", {"request": request, "user": user, "data": data}
    )


@router.get("/")
async def get_index(
    request: Request, user: User | None = Depends(get_correct_user_frontend)
):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
