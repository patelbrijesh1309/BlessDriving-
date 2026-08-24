from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.language_repository import LanguageRepository
from app.repositories.student_language_repository import StudentLanguageRepository
from app.repositories.student_repository import StudentRepository


class StudentLanguageService:

    @staticmethod
    async def update_languages(
        db: AsyncSession,
        student_id: int,
        language_ids: list[int],
        primary_language_id: int,
    ):
        student = await StudentRepository.get_by_id(db, student_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student profile not found.",
            )

        if primary_language_id not in language_ids:
            raise HTTPException(
                status_code=400,
                detail="Primary language must be included in language_ids.",
            )

        languages = await LanguageRepository.get_by_ids(db, language_ids)

        if len(languages) != len(set(language_ids)):
            raise HTTPException(
                status_code=400,
                detail="One or more languages are invalid.",
            )

        await StudentLanguageRepository.replace_languages(
            db,
            student_id,
            language_ids,
            primary_language_id,
        )

        await db.commit()

        return {"message": "Languages updated successfully."}

    @staticmethod
    async def get_languages(
        db: AsyncSession,
        student_id: int,
    ):
        records = await StudentLanguageRepository.get_languages(
            db,
            student_id,
        )

        return [
            {
                "id": record.language.id,
                "name": record.language.name,
                "code": record.language.code,
                "is_primary": record.is_primary,
            }
            for record in records
        ]