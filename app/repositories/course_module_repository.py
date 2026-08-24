from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course_module import CourseModule
from app.schemas.course_module import (
    CourseModuleCreate,
    CourseModuleUpdate,
)


class CourseModuleRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: CourseModuleCreate,
    ):

        module = CourseModule(**data.model_dump())

        db.add(module)
        await db.commit()
        await db.refresh(module)

        return module

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        module_id: int,
    ):

        result = await db.execute(
            select(CourseModule).where(CourseModule.id == module_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_course(
        db: AsyncSession,
        course_id: int,
    ):

        result = await db.execute(
            select(CourseModule)
            .where(CourseModule.course_id == course_id)
            .order_by(CourseModule.order_number)
        )

        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession,
        module: CourseModule,
        data: CourseModuleUpdate,
    ):

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(module, key, value)

        await db.commit()
        await db.refresh(module)

        return module

    @staticmethod
    async def delete(
        db: AsyncSession,
        module: CourseModule,
    ):

        await db.delete(module)
        await db.commit()