from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)


class AuthService:

    @staticmethod
    async def register(
        db: AsyncSession,
        data: RegisterRequest,
    ):
        existing = await UserRepository.get_by_email(
            db,
            data.email,
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already registered.",
            )

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=True,
        )

        return await UserRepository.create(
            db,
            user,
        )

    @staticmethod
    async def login(
        db: AsyncSession,
        data: LoginRequest,
    ):
        user = await UserRepository.get_by_email(
            db,
            data.email,
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }