from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.course_repository import CourseRepository
from app.repositories.student_enrollment_repository import (
    StudentEnrollmentRepository,
)
from app.repositories.student_repository import StudentRepository
from app.schemas.student_enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
)


class StudentEnrollmentService:

    @staticmethod
    async def create_enrollment(
        db: AsyncSession,
        data: EnrollmentCreate,
    ):
        student = await StudentRepository.get_by_id(db, data.student_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        course = await CourseRepository.get_by_id(db, data.course_id)

        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course not found.",
            )

        existing = await StudentEnrollmentRepository.get_existing(
            db,
            data.student_id,
            data.course_id,
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Student is already enrolled in this course.",
            )

        return await StudentEnrollmentRepository.create(db, data)

    @staticmethod
    async def get_student_enrollments(
        db: AsyncSession,
        student_id: int,
    ):
        return await StudentEnrollmentRepository.get_by_student(
            db,
            student_id,
        )

    @staticmethod
    async def update_enrollment(
        db: AsyncSession,
        enrollment_id: int,
        data: EnrollmentUpdate,
    ):
        enrollment = await StudentEnrollmentRepository.get_by_id(
            db,
            enrollment_id,
        )

        if enrollment is None:
            raise HTTPException(
                status_code=404,
                detail="Enrollment not found.",
            )

        return await StudentEnrollmentRepository.update(
            db,
            enrollment,
            data,
        )

    @staticmethod
    async def delete_enrollment(
        db: AsyncSession,
        enrollment_id: int,
    ):
        enrollment = await StudentEnrollmentRepository.get_by_id(
            db,
            enrollment_id,
        )

        if enrollment is None:
            raise HTTPException(
                status_code=404,
                detail="Enrollment not found.",
            )

        await StudentEnrollmentRepository.delete(
            db,
            enrollment,
        )

        return {"message": "Enrollment deleted successfully."}