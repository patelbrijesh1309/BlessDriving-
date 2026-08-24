from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.student_language import StudentLanguage


class StudentLanguageRepository:

    @staticmethod
    async def replace_languages(
        db: AsyncSession,
        student_id: int,
        language_ids: list[int],
        primary_language_id: int,
    ):
        await db.execute(
            delete(StudentLanguage).where(
                StudentLanguage.student_id == student_id
            )
        )

        for language_id in language_ids:
            db.add(
                StudentLanguage(
                    student_id=student_id,
                    language_id=language_id,
                    is_primary=language_id == primary_language_id,
                )
            )

        await db.flush()

    @staticmethod
    async def get_languages(
        db: AsyncSession,
        student_id: int,
    ):
        result = await db.execute(
            select(StudentLanguage)
            .options(selectinload(StudentLanguage.language))
            .where(StudentLanguage.student_id == student_id)
        )

        return result.scalars().all()