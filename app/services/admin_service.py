from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.instructor import Instructor
from app.models.student import Student
from app.models.user import User
from app.repositories.instructor_repository import InstructorRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import (
    AdminCreateInstructorRequest,
    AdminCreateStudentRequest,
    AdminUpdateInstructorRequest,
    AdminUpdateStudentRequest,
)


class AdminService:

    # ===================== STUDENTS =====================

    @staticmethod
    async def create_student(
        db: AsyncSession,
        data: AdminCreateStudentRequest,
    ):
        try:
            user = await UserRepository.get_by_email(db, data.email)

            role = await UserRepository.get_role_by_name(db, "STUDENT")

            if role is None:
                raise HTTPException(
                    status_code=500,
                    detail="STUDENT role not found.",
                )

            if user is None:
                user = User(
                    email=data.email,
                    password_hash=hash_password(data.password),
                    first_name=data.first_name,
                    last_name=data.last_name,
                    is_active=True,
                )

                await UserRepository.add(db, user)

            existing_student = await StudentRepository.get_by_id(
                db,
                user.id,
            )

            if existing_student:
                raise HTTPException(
                    status_code=400,
                    detail="Student profile already exists.",
                )

            await UserRepository.add_role(
                db,
                user,
                role,
            )

            student = Student(
                user_id=user.id,
                phone=data.phone,
                date_of_birth=data.date_of_birth,
                address=data.address,
                pickup_address=data.pickup_address,
                emergency_contact=data.emergency_contact,
                notes=data.notes,
            )

            await StudentRepository.add(db, student)

            await db.commit()
            await db.refresh(user)
            await db.refresh(student)

            return {
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": "STUDENT",
                "phone": student.phone,
                "date_of_birth": student.date_of_birth,
                "address": student.address,
                "pickup_address": student.pickup_address,
                "emergency_contact": student.emergency_contact,
                "notes": student.notes,
                "is_active": user.is_active,
            }

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_students(
        db: AsyncSession,
        page: int = 1,
        limit: int = 10,
    ):
        students, total = await StudentRepository.get_paginated(
            db,
            page,
            limit,
        )

        return {
            "items": [
                {
                    "user_id": s.user_id,
                    "email": s.user.email,
                    "first_name": s.user.first_name,
                    "last_name": s.user.last_name,
                    "phone": s.phone,
                    "date_of_birth": s.date_of_birth,
                    "address": s.address,
                    "pickup_address": s.pickup_address,
                    "emergency_contact": s.emergency_contact,
                    "notes": s.notes,
                    "is_active": s.user.is_active,
                }
                for s in students
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }

    @staticmethod
    async def get_student_by_id(
        db: AsyncSession,
        user_id: int,
    ):
        student = await StudentRepository.get_by_id(db, user_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        return student

    @staticmethod
    async def update_student(
        db: AsyncSession,
        user_id: int,
        data: AdminUpdateStudentRequest,
    ):
        student = await StudentRepository.get_by_id(db, user_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        updated = await StudentRepository.update(
            db,
            student,
            data,
        )

        await db.commit()

        return updated

    @staticmethod
    async def delete_student(
        db: AsyncSession,
        user_id: int,
    ):
        student = await StudentRepository.get_by_id(db, user_id)

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        await StudentRepository.delete(db, student)
        await db.commit()

        return {"message": "Student deleted successfully."}

    # ===================== INSTRUCTORS =====================

    @staticmethod
    async def create_instructor(
        db: AsyncSession,
        data: AdminCreateInstructorRequest,
    ):
        try:
            user = await UserRepository.get_by_email(
                db,
                data.email,
            )

            role = await UserRepository.get_role_by_name(
                db,
                "INSTRUCTOR",
            )

            if role is None:
                raise HTTPException(
                    status_code=500,
                    detail="INSTRUCTOR role not found.",
                )

            if user is None:
                user = User(
                    email=data.email,
                    password_hash=hash_password(data.password),
                    first_name=data.first_name,
                    last_name=data.last_name,
                    is_active=True,
                )

                await UserRepository.add(db, user)

            existing_instructor = await InstructorRepository.get_by_id(
                db,
                user.id,
            )

            if existing_instructor:
                raise HTTPException(
                    status_code=400,
                    detail="Instructor profile already exists.",
                )

            await UserRepository.add_role(
                db,
                user,
                role,
            )

            instructor = Instructor(
                user_id=user.id,
                phone=data.phone,
                license_number=data.license_number,
                hire_date=data.hire_date,
                employment_type=data.employment_type,
                hourly_rate=data.hourly_rate,
                is_active=True,
            )

            await InstructorRepository.add(db, instructor)

            await db.commit()
            await db.refresh(user)
            await db.refresh(instructor)

            return {
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": "INSTRUCTOR",
                "phone": instructor.phone,
                "license_number": instructor.license_number,
                "hire_date": instructor.hire_date,
                "employment_type": instructor.employment_type,
                "hourly_rate": str(instructor.hourly_rate),
                "is_active": instructor.is_active,
            }

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_instructors(
        db: AsyncSession,
        page: int = 1,
        limit: int = 10,
    ):
        instructors, total = await InstructorRepository.get_paginated(
            db,
            page,
            limit,
        )

        return {
            "items": [
                {
                    "user_id": i.user_id,
                    "email": i.user.email,
                    "first_name": i.user.first_name,
                    "last_name": i.user.last_name,
                    "phone": i.phone,
                    "license_number": i.license_number,
                    "hire_date": i.hire_date,
                    "employment_type": i.employment_type,
                    "hourly_rate": str(i.hourly_rate),
                    "is_active": i.is_active,
                }
                for i in instructors
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }

    @staticmethod
    async def get_instructor_by_id(
        db: AsyncSession,
        user_id: int,
    ):
        instructor = await InstructorRepository.get_by_id(
            db,
            user_id,
        )

        if instructor is None:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found.",
            )

        return instructor

    @staticmethod
    async def update_instructor(
        db: AsyncSession,
        user_id: int,
        data: AdminUpdateInstructorRequest,
    ):
        instructor = await InstructorRepository.get_by_id(
            db,
            user_id,
        )

        if instructor is None:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found.",
            )

        updated = await InstructorRepository.update(
            db,
            instructor,
            data,
        )

        await db.commit()

        return updated

    @staticmethod
    async def delete_instructor(
        db: AsyncSession,
        user_id: int,
    ):
        instructor = await InstructorRepository.get_by_id(
            db,
            user_id,
        )

        if instructor is None:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found.",
            )

        await InstructorRepository.delete(db, instructor)
        await db.commit()

        return {"message": "Instructor deleted successfully."}

    # ===================== DASHBOARD =====================

    @staticmethod
    async def get_dashboard(db: AsyncSession):
        return {
            "total_users": await UserRepository.count_users(db),
            "total_students": await StudentRepository.count_students(db),
            "total_instructors": await InstructorRepository.count_instructors(db),
        }

    @classmethod
    async def create_user(cls, db, data):
        pass