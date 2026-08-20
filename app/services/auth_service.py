from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest


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