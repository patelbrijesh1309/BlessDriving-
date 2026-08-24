from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.course_module_repository import (
    CourseModuleRepository,
)
from app.repositories.course_repository import CourseRepository
from app.schemas.course_module import (
    CourseModuleCreate,
    CourseModuleUpdate,
)


class CourseModuleService:

    @staticmethod
    async def create_module(
        db: AsyncSession,
        data: CourseModuleCreate,
    ):

        course = await CourseRepository.get_by_id(db, data.course_id)

        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course not found.",
            )

        return await CourseModuleRepository.create(db, data)

    @staticmethod
    async def get_course_modules(
        db: AsyncSession,
        course_id: int,
    ):

        return await CourseModuleRepository.get_by_course(
            db,
            course_id,
        )

    @staticmethod
    async def get_module(
        db: AsyncSession,
        module_id: int,
    ):

        module = await CourseModuleRepository.get_by_id(
            db,
            module_id,
        )

        if module is None:
            raise HTTPException(
                status_code=404,
                detail="Course module not found.",
            )

        return module

    @staticmethod
    async def update_module(
        db: AsyncSession,
        module_id: int,
        data: CourseModuleUpdate,
    ):

        module = await CourseModuleRepository.get_by_id(
            db,
            module_id,
        )

        if module is None:
            raise HTTPException(
                status_code=404,
                detail="Course module not found.",
            )

        return await CourseModuleRepository.update(
            db,
            module,
            data,
        )

    @staticmethod
    async def delete_module(
        db: AsyncSession,
        module_id: int,
    ):

        module = await CourseModuleRepository.get_by_id(
            db,
            module_id,
        )

        if module is None:
            raise HTTPException(
                status_code=404,
                detail="Course module not found.",
            )

        await CourseModuleRepository.delete(db, module)

        return {"message": "Course module deleted successfully."}