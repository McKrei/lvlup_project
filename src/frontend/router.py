from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from user.dependency import get_correct_user_frontend, get_current_user
from .dependency import get_user_or_redirect
from database.models import User
from portfolio.crud import CRUDPortfolio


router = APIRouter(prefix="", tags=["frontend"])

templates = Jinja2Templates(directory="frontend/template")


@router.get("/register/")
async def get_register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/auth/")
async def get_login(
    request: Request,
    user: User | None = Depends(get_correct_user_frontend),
    not_auth: bool | None = None,
):

    return templates.TemplateResponse(
        "auth/auth.html", {"request": request, "not_auth": not_auth}
    )


@router.get("/logout/", response_class=RedirectResponse)
async def get_logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/")
async def get_index(
    request: Request, user: User | None = Depends(get_correct_user_frontend)
):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.get("/assert")
async def get_assert(request: Request, user: User = Depends(get_user_or_redirect)):
    return templates.TemplateResponse(
        "pages/assert.html", {"request": request, "user": user}
    )


@router.get("/portfolio")
async def get_portfolio(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    session: AsyncSession = Depends(get_session),
):

    data = await CRUDPortfolio.get_all_by_user_id(session, user.id)
    return templates.TemplateResponse(
        "pages/portfolio.html", {"request": request, "user": user, "data": data}
    )


@router.post("/portfolio")
async def create_portfolio(
    request: Request,
    user: User = Depends(get_user_or_redirect),
    name: str = Form(...),
    description: str = Form(""),
    session: AsyncSession = Depends(get_session),
):
    data = {"name": name, "description": description, "user_id": user.id}
    await CRUDPortfolio.create(session, data)
    return RedirectResponse(url="/portfolio", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/profile")
async def get_profile(request: Request, user: User = Depends(get_user_or_redirect)):
    return templates.TemplateResponse(
        "pages/profile.html", {"request": request, "user": user}
    )


@router.get("/transaction")
async def get_transaction(request: Request, user: User = Depends(get_user_or_redirect)):
    return templates.TemplateResponse(
        "pages/transaction.html", {"request": request, "user": user}
    )
