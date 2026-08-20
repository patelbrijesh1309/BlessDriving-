from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: StudentCreate,
    ) -> Student:

        student = Student(**data.model_dump())

        db.add(student)

        await db.commit()
        await db.refresh(student)

        return student

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        user_id: int,
    ):

        result = await db.execute(
            select(Student).where(Student.user_id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(select(Student))

        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession,
        student: Student,
        data: StudentUpdate,
    ):

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(student, key, value)

        await db.commit()
        await db.refresh(student)

        return student

    @staticmethod
    async def delete(
        db: AsyncSession,
        student: Student,
    ):

        await db.delete(student)
        await db.commit()