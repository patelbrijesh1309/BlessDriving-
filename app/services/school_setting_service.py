from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.school_setting_repository import (
    SchoolSettingRepository,
)
from app.schemas.school_setting import SchoolSettingUpdate


class SchoolSettingService:

    @staticmethod
    async def get_settings(db: AsyncSession):
        setting = await SchoolSettingRepository.get(db)

        if setting is None:
            setting = await SchoolSettingRepository.create_default(db)

        return setting

    @staticmethod
    async def update_settings(
        db: AsyncSession,
        data: SchoolSettingUpdate,
    ):
        setting = await SchoolSettingRepository.get(db)

        if setting is None:
            setting = await SchoolSettingRepository.create_default(db)

        return await SchoolSettingRepository.update(
            db,
            setting,
            data,
        )