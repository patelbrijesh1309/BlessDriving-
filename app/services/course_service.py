from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate


class CourseService:

    @staticmethod
    async def create_course(
        db: AsyncSession,
        data: CourseCreate,
    ):

        if await CourseRepository.get_by_name(db, data.name):
            raise HTTPException(
                status_code=400,
                detail="Course already exists.",
            )

        return await CourseRepository.create(db, data)

    @staticmethod
    async def get_courses(db: AsyncSession):

        return await CourseRepository.get_all(db)

    @staticmethod
    async def get_course(
        db: AsyncSession,
        course_id: int,
    ):

        course = await CourseRepository.get_by_id(db, course_id)

        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course not found.",
            )

        return course

    @staticmethod
    async def update_course(
        db: AsyncSession,
        course_id: int,
        data: CourseUpdate,
    ):

        course = await CourseRepository.get_by_id(db, course_id)

        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course not found.",
            )

        return await CourseRepository.update(db, course, data)

    @staticmethod
    async def delete_course(
        db: AsyncSession,
        course_id: int,
    ):

        course = await CourseRepository.get_by_id(db, course_id)

        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course not found.",
            )

        await CourseRepository.delete(db, course)

        return {"message": "Course deleted successfully."}