from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:

    @staticmethod
    async def create_student(
        db: AsyncSession,
        data: StudentCreate,
    ):
        existing = await StudentRepository.get_by_id(db, data.user_id)

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Student already exists.",
            )

        return await StudentRepository.create(db, data)

    @staticmethod
    async def get_student(
        db: AsyncSession,
        user_id: int,
    ):
        student = await StudentRepository.get_by_id(db, user_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        return student

    @staticmethod
    async def get_students(db: AsyncSession):
        return await StudentRepository.get_all(db)

    @staticmethod
    async def update_student(
        db: AsyncSession,
        user_id: int,
        data: StudentUpdate,
    ):
        student = await StudentRepository.get_by_id(db, user_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        return await StudentRepository.update(db, student, data)

    @staticmethod
    async def delete_student(
        db: AsyncSession,
        user_id: int,
    ):
        student = await StudentRepository.get_by_id(db, user_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        await StudentRepository.delete(db, student)

        return {"message": "Student deleted successfully."}