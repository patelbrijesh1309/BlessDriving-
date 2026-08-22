
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.instructor import Instructor
from app.schemas.instructor import InstructorCreate, InstructorUpdate


class InstructorRepository:

    @staticmethod
    async def create(db: AsyncSession, data: InstructorCreate):
        instructor = Instructor(**data.model_dump())

        db.add(instructor)
        await db.commit()
        await db.refresh(instructor)

        return instructor

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(Instructor).where(Instructor.user_id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Instructor))

        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession,
        instructor: Instructor,
        data: InstructorUpdate,
    ):
        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(instructor, key, value)

        await db.commit()
        await db.refresh(instructor)

        return instructor

    @staticmethod
    async def delete(
        db: AsyncSession,
        instructor: Instructor,
    ):
        await db.delete(instructor)
        await db.commit()

    @staticmethod
    async def add(
        db: AsyncSession,
        instructor: Instructor,
    ):
        db.add(instructor)
        await db.flush()
        await db.refresh(instructor)
        return instructor

    @staticmethod
    async def get_paginated(
        db: AsyncSession,
        page: int = 1,
        limit: int = 10,
    ):
        offset = (page - 1) * limit

        total = await db.scalar(
            select(func.count()).select_from(Instructor)
        )

        result = await db.execute(
            select(Instructor)
            .options(selectinload(Instructor.user))
            .offset(offset)
            .limit(limit)
        )

        instructors = result.scalars().all()

        return instructors, total or 0

    @staticmethod
    async def get_by_user_id(
        db: AsyncSession,
        user_id: int,
    ):
        result = await db.execute(
            select(Instructor)
            .options(selectinload(Instructor.user))
            .where(Instructor.user_id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def count_instructors(db: AsyncSession):
        return await db.scalar(
            select(func.count()).select_from(Instructor)
        ) or 0


    @staticmethod
    async def count_active_instructors(db: AsyncSession):
        result = await db.execute(
            select(func.count())
            .select_from(Instructor)
            .join(Instructor.user)
            .where(User.is_active == True)
        )

        return result.scalar() or 0