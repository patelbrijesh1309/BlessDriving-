from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.register(db, data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.login(db, data)


# NEW ENDPOINT (Swagger OAuth2 ke liye)
@router.post(
    "/token",
    response_model=TokenResponse,
    summary="OAuth2 form login (Swagger)",
)
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.login(
        db,
        LoginRequest(
            email=form_data.username,
            password=form_data.password,
        ),
    )