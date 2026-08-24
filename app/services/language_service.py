from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.language_repository import LanguageRepository
from app.schemas.language import (
    LanguageCreate,
    LanguageUpdate,
)


class LanguageService:

    @staticmethod
    async def create_language(
        db: AsyncSession,
        data: LanguageCreate,
    ):
        existing_name = await LanguageRepository.get_by_name(
            db,
            data.name,
        )

        if existing_name:
            raise HTTPException(
                status_code=400,
                detail="Language name already exists.",
            )

        existing_code = await LanguageRepository.get_by_code(
            db,
            data.code,
        )

        if existing_code:
            raise HTTPException(
                status_code=400,
                detail="Language code already exists.",
            )

        return await LanguageRepository.create(
            db,
            data,
        )

    @staticmethod
    async def get_languages(db: AsyncSession):
        return await LanguageRepository.get_all(db)

    @staticmethod
    async def get_language(
        db: AsyncSession,
        language_id: int,
    ):
        language = await LanguageRepository.get_by_id(
            db,
            language_id,
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found.",
            )

        return language

    @staticmethod
    async def update_language(
        db: AsyncSession,
        language_id: int,
        data: LanguageUpdate,
    ):
        language = await LanguageRepository.get_by_id(
            db,
            language_id,
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found.",
            )

        existing_name = await LanguageRepository.get_by_name(
            db,
            data.name,
        )

        if existing_name and existing_name.id != language.id:
            raise HTTPException(
                status_code=400,
                detail="Language name already exists.",
            )

        existing_code = await LanguageRepository.get_by_code(
            db,
            data.code,
        )

        if existing_code and existing_code.id != language.id:
            raise HTTPException(
                status_code=400,
                detail="Language code already exists.",
            )

        return await LanguageRepository.update(
            db,
            language,
            data,
        )

    @staticmethod
    async def delete_language(
        db: AsyncSession,
        language_id: int,
    ):
        language = await LanguageRepository.get_by_id(
            db,
            language_id,
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found.",
            )

        await LanguageRepository.delete(
            db,
            language,
        )

        return {"message": "Language deleted successfully."}