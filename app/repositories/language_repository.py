from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.language import Language
from app.schemas.language import LanguageCreate, LanguageUpdate


class LanguageRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: LanguageCreate,
    ) -> Language:

        language = Language(**data.model_dump())

        db.add(language)

        await db.commit()
        await db.refresh(language)

        return language

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(Language).order_by(Language.name)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        language_id: int,
    ):

        result = await db.execute(
            select(Language).where(Language.id == language_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_ids(
        db: AsyncSession,
        language_ids: list[int],
    ):

        result = await db.execute(
            select(Language).where(
                Language.id.in_(language_ids)
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_name(
        db: AsyncSession,
        name: str,
    ):

        result = await db.execute(
            select(Language).where(Language.name == name)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_code(
        db: AsyncSession,
        code: str,
    ):

        result = await db.execute(
            select(Language).where(Language.code == code)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        language: Language,
        data: LanguageUpdate,
    ):

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(language, key, value)

        await db.commit()
        await db.refresh(language)

        return language

    @staticmethod
    async def delete(
        db: AsyncSession,
        language: Language,
    ):

        await db.delete(language)
        await db.commit()