from datetime import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school_setting import SchoolSetting
from app.schemas.school_setting import SchoolSettingUpdate


class SchoolSettingRepository:

    @staticmethod
    async def get(db: AsyncSession):
        result = await db.execute(select(SchoolSetting))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_default(db: AsyncSession):
        setting = SchoolSetting(
            school_name="Bless Driving",
            opening_time=time(8, 0),
            closing_time=time(18, 0),
            default_lesson_duration=60,
            buffer_minutes=15,
            cancellation_hours=24,
            timezone="Australia/Sydney",
        )

        db.add(setting)
        await db.commit()
        await db.refresh(setting)

        return setting

    @staticmethod
    async def update(
        db: AsyncSession,
        setting: SchoolSetting,
        data: SchoolSettingUpdate,
    ):
        values = data.model_dump()

        for key, value in values.items():
            setattr(setting, key, value)

        await db.commit()
        await db.refresh(setting)

        return setting