from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student_enrollment import StudentEnrollment
from app.schemas.student_enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
)


class StudentEnrollmentRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: EnrollmentCreate,
    ):
        enrollment = StudentEnrollment(**data.model_dump())

        db.add(enrollment)
        await db.commit()
        await db.refresh(enrollment)

        return enrollment

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        enrollment_id: int,
    ):
        result = await db.execute(
            select(StudentEnrollment).where(
                StudentEnrollment.id == enrollment_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_student(
        db: AsyncSession,
        student_id: int,
    ):
        result = await db.execute(
            select(StudentEnrollment).where(
                StudentEnrollment.student_id == student_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def get_existing(
        db: AsyncSession,
        student_id: int,
        course_id: int,
    ):
        result = await db.execute(
            select(StudentEnrollment).where(
                StudentEnrollment.student_id == student_id,
                StudentEnrollment.course_id == course_id,
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        enrollment: StudentEnrollment,
        data: EnrollmentUpdate,
    ):
        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(enrollment, key, value)

        await db.commit()
        await db.refresh(enrollment)

        return enrollment

    @staticmethod
    async def delete(
        db: AsyncSession,
        enrollment: StudentEnrollment,
    ):
        await db.delete(enrollment)
        await db.commit()