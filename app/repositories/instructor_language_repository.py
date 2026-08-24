from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.instructor_language import InstructorLanguage


class InstructorLanguageRepository:

    @staticmethod
    async def get_by_instructor(
        db: AsyncSession,
        instructor_id: int,
    ):
        result = await db.execute(
            select(InstructorLanguage)
            .options(selectinload(InstructorLanguage.language))
            .where(
                InstructorLanguage.instructor_id == instructor_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def replace_languages(
        db: AsyncSession,
        instructor_id: int,
        languages: list[InstructorLanguage],
    ):
        await db.execute(
            delete(InstructorLanguage).where(
                InstructorLanguage.instructor_id == instructor_id
            )
        )

        db.add_all(languages)

        await db.commit()