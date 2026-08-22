from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.user import User

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
    async def create_model(
        db: AsyncSession,
        student: Student,
    ) -> Student:

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
            select(Student)
            .options(selectinload(Student.user))
            .where(Student.user_id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ):

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

    @staticmethod
    async def add(
        db: AsyncSession,
        student: Student,
    ):

        db.add(student)
        await db.flush()
        await db.refresh(student)

        return student

    @staticmethod
    async def get_paginated(
        db: AsyncSession,
        page: int = 1,
        limit: int = 10,
    ):

        offset = (page - 1) * limit

        total = await db.scalar(
            select(func.count()).select_from(Student)
        )

        result = await db.execute(
            select(Student)
            .options(selectinload(Student.user))
            .offset(offset)
            .limit(limit)
        )

        students = result.scalars().all()

        return students, total or 0

    @staticmethod
    async def update_admin(
        db: AsyncSession,
        student: Student,
        user: User,
        data,
    ):
        values = data.model_dump(exclude_unset=True)

        user_fields = {
            "first_name",
            "last_name",
            "is_active",
        }

        for key, value in values.items():
            if key in user_fields:
                setattr(user, key, value)
            else:
                setattr(student, key, value)

        await db.commit()
        await db.refresh(user)
        await db.refresh(student)

        return student

    @staticmethod
    async def delete(
        db: AsyncSession,
        student: Student,
    ):
        await db.delete(student)

    @staticmethod
    async def count_students(db: AsyncSession):
        return await db.scalar(
            select(func.count()).select_from(Student)
        ) or 0

    @staticmethod
    async def count_active_students(db: AsyncSession):
        result = await db.execute(
            select(func.count())
            .select_from(Student)
            .join(Student.user)
            .where(User.is_active == True)
        )
        return result.scalar() or 0