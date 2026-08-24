from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.instructor_language import InstructorLanguage
from app.repositories.instructor_language_repository import (
    InstructorLanguageRepository,
)
from app.repositories.language_repository import LanguageRepository
from app.repositories.instructor_repository import (
    InstructorRepository,
)
from app.schemas.instructor_language import (
    InstructorLanguageUpdate,
)


class InstructorLanguageService:

    @staticmethod
    async def get_my_languages(
        db: AsyncSession,
        instructor_id: int,
    ):
        rows = await InstructorLanguageRepository.get_by_instructor(
            db,
            instructor_id,
        )

        return [
            {
                "id": row.language.id,
                "name": row.language.name,
                "code": row.language.code,
                "is_primary": row.is_primary,
            }
            for row in rows
        ]

    @staticmethod
    async def update_my_languages(
        db: AsyncSession,
        instructor_id: int,
        data: InstructorLanguageUpdate,
    ):
        instructor = await InstructorRepository.get_by_id(
            db,
            instructor_id,
        )

        if instructor is None:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found.",
            )

        models = []

        for language_id in data.language_ids:

            language = await LanguageRepository.get_by_id(
                db,
                language_id,
            )

            if language is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Language {language_id} not found.",
                )

            models.append(
                InstructorLanguage(
                    instructor_id=instructor_id,
                    language_id=language_id,
                    is_primary=(
                        language_id == data.primary_language_id
                    ),
                )
            )

        await InstructorLanguageRepository.replace_languages(
            db,
            instructor_id,
            models,
        )

        return await InstructorLanguageService.get_my_languages(
            db,
            instructor_id,
        )