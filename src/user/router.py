from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, Response

from database.database import get_session
from database.models import User
from .schemas import UserCreate, UserOut
from .crud import CRUDUser
from .auth import hash_password, verify_password, create_access_token
from .dependency import get_current_user, get_user_by_id
from .exceptions import exception_user_not_found, exception_auth, exception_unique_field


router = APIRouter(prefix="/user", tags=["users"])


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await CRUDUser.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise exception_auth
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth")
async def login_for_access_token_frontend(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await CRUDUser.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        return RedirectResponse(url="/auth?not_auth=true", status_code=status.HTTP_303_SEE_OTHER)
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token)
    return response



@router.post("/register")
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    password = hash_password(password)
    data = {"username": username, "password": password, "email": email}
    user = await CRUDUser.create(session, data)
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token)
    return response

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    """
    Создание нового пользователя.
    """
    user.password = hash_password(user.password)
    new_user = await CRUDUser.create(session, user.model_dump())
    if new_user is None:
        raise exception_unique_field
    return new_user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Получение информации о пользователе по ID.
    """
    return user


@router.get("/", response_model=list[UserOut])
async def get_users(session: AsyncSession = Depends(get_session)):
    """
    Получение списка всех пользователей.
    """
    users = await CRUDUser.get_all(session)
    return users


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_data: UserCreate,
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_session),
):
    """
    Обновление данных пользователя по ID.
    """
    if user_data.password:
        user_data.password = hash_password(user_data.password)
    updated_user = await CRUDUser.update(session, user, user_data.model_dump())
    if updated_user is None:
        raise exception_unique_field
    return updated_user
