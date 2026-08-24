from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


class CourseRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: CourseCreate,
    ) -> Course:

        course = Course(**data.model_dump())

        db.add(course)
        await db.commit()
        await db.refresh(course)

        return course

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(Course).order_by(Course.name)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        course_id: int,
    ):

        result = await db.execute(
            select(Course).where(Course.id == course_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(
        db: AsyncSession,
        name: str,
    ):

        result = await db.execute(
            select(Course).where(Course.name == name)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        course: Course,
        data: CourseUpdate,
    ):

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(course, key, value)

        await db.commit()
        await db.refresh(course)

        return course

    @staticmethod
    async def delete(
        db: AsyncSession,
        course: Course,
    ):

        await db.delete(course)
        await db.commit()