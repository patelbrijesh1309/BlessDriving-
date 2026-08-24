from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


class UserRepository:

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ):
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == email)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        user_id: int,
    ):
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db: AsyncSession,
        user: User,
    ):
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def add(
        db: AsyncSession,
        user: User,
    ):
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_role_by_name(
        db: AsyncSession,
        role_name: str,
    ):
        result = await db.execute(
            select(Role).where(Role.name == role_name)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def add_role(
        db: AsyncSession,
        user: User,
        role: Role,
    ):
        result = await db.execute(
            select(UserRole).where(
                UserRole.user_id == user.id,
                UserRole.role_id == role.id,
            )
        )

        existing = result.scalar_one_or_none()

        if existing is None:
            db.add(
                UserRole(
                    user_id=user.id,
                    role_id=role.id,
                )
            )
            await db.flush()

    @staticmethod
    async def delete(
        db: AsyncSession,
        user: User,
    ):
        await db.delete(user)

    @staticmethod
    async def count_users(
        db: AsyncSession,
    ):
        return (
            await db.scalar(
                select(func.count()).select_from(User)
            )
            or 0
        )