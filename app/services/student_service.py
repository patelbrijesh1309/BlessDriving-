from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentRegisterRequest,
)


class StudentService:

    @staticmethod
    async def register_student(
        db: AsyncSession,
        data: StudentRegisterRequest,
    ):
        try:
            existing_user = await UserRepository.get_by_email(
                db,
                data.email,
            )

            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists.",
                )

            role = await UserRepository.get_role_by_name(
                db,
                "STUDENT",
            )

            if role is None:
                raise HTTPException(
                    status_code=500,
                    detail="STUDENT role not found.",
                )

            user = User(
                email=data.email,
                password_hash=hash_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name,
                is_active=True,
            )

            await UserRepository.add(db, user)
            await UserRepository.add_role(db, user, role)

            student_data = StudentCreate(
                user_id=user.id,
                phone=data.phone,
                date_of_birth=data.date_of_birth,
                address=data.address,
                pickup_address=data.pickup_address,
                emergency_contact=data.emergency_contact,
                notes=data.notes,
            )

            await StudentRepository.create(db, student_data)

            await db.commit()

            return {
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": "STUDENT",
            }

        except Exception:
            await db.rollback()
            raise

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