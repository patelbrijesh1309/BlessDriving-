from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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