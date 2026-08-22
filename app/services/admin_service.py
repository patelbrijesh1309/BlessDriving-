from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.admin_student import AdminUpdateStudentRequest

from app.core.security import hash_password

from app.models.user import User
from app.models.student import Student
from app.models.instructor import Instructor

from app.repositories.user_repository import UserRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.instructor_repository import InstructorRepository
from app.schemas.instructor import InstructorUpdate
from app.schemas.admin import AdminCreateUserRequest
from app.schemas.admin_student import AdminCreateStudentRequest
from app.schemas.instructor import AdminCreateInstructorRequest


class AdminService:

    VALID_ROLES = {
        "ADMIN",
        "SCHEDULER",
        "INSTRUCTOR",
        "STUDENT",

    }

    @staticmethod
    async def create_user(
        db: AsyncSession,
        data: AdminCreateUserRequest,
    ):
        try:
            existing = await UserRepository.get_by_email(db, data.email)

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists.",
                )

            role_name = data.role.upper()

            if role_name not in AdminService.VALID_ROLES:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid role.",
                )

            role = await UserRepository.get_role_by_name(db, role_name)

            if role is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"Role '{role_name}' not found.",
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

            await db.commit()
            await db.refresh(user)

            return {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": role.name,
                "is_active": user.is_active,
            }

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def create_student(
        db: AsyncSession,
        data: AdminCreateStudentRequest,
    ):
        try:
            existing = await UserRepository.get_by_email(db, data.email)

            if existing:
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
    async def create_instructor(
        db: AsyncSession,
        data: AdminCreateInstructorRequest,
    ):
        try:
            existing = await UserRepository.get_by_email(
                db,
                data.email,
            )

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists.",
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

            user = User(
                email=data.email,
                password_hash=hash_password(data.password),
                first_name=data.first_name,
                last_name=data.last_name,
                is_active=True,
            )

            await UserRepository.add(db, user)
            await UserRepository.add_role(db, user, role)

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
                    "user_id": instructor.user_id,
                    "email": instructor.user.email,
                    "first_name": instructor.user.first_name,
                    "last_name": instructor.user.last_name,
                    "phone": instructor.phone,
                    "license_number": instructor.license_number,
                    "hire_date": instructor.hire_date,
                    "employment_type": instructor.employment_type,
                    "hourly_rate": instructor.hourly_rate,
                    "is_active": instructor.user.is_active,
                }
                for instructor in instructors
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }

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

        return {
            "user_id": student.user_id,
            "email": student.user.email,
            "first_name": student.user.first_name,
            "last_name": student.user.last_name,
            "role": "STUDENT",
            "phone": student.phone,
            "date_of_birth": student.date_of_birth,
            "address": student.address,
            "pickup_address": student.pickup_address,
            "emergency_contact": student.emergency_contact,
            "notes": student.notes,
            "is_active": student.user.is_active,
        } 

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

        await StudentRepository.update_admin(
            db,
            student,
            student.user,
            data,
        )

        return {
            "user_id": student.user_id,
            "email": student.user.email,
            "first_name": student.user.first_name,
            "last_name": student.user.last_name,
            "role": "STUDENT",
            "phone": student.phone,
            "date_of_birth": student.date_of_birth,
            "address": student.address,
            "pickup_address": student.pickup_address,
            "emergency_contact": student.emergency_contact,
            "notes": student.notes,
            "is_active": student.user.is_active,
        }

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

        # Sirf User delete karo.
        # Student cascade se automatically delete ho jayega.
        await UserRepository.delete(db, student.user)

        await db.commit()

        return {
            "message": "Student deleted successfully."
        }

    @staticmethod
    async def get_instructor(
        db: AsyncSession,
        user_id: int,
    ):
        instructor = await InstructorRepository.get_by_user_id(
            db,
            user_id,
        )

        if instructor is None:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found.",
            )

        return {
            "user_id": instructor.user_id,
            "email": instructor.user.email,
            "first_name": instructor.user.first_name,
            "last_name": instructor.user.last_name,
            "phone": instructor.phone,
            "license_number": instructor.license_number,
            "hire_date": instructor.hire_date,
            "employment_type": instructor.employment_type,
            "hourly_rate": str(instructor.hourly_rate),
            "is_active": instructor.user.is_active,
        }


    @staticmethod
    async def update_instructor(
        db: AsyncSession,
        user_id: int,
        data: InstructorUpdate,
    ):
        instructor = await InstructorRepository.get_by_user_id(db, user_id)

        if instructor is None:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found.",
            )

        await InstructorRepository.update(
            db,
            instructor,
            data,
        )

        return {
            "user_id": instructor.user_id,
            "email": instructor.user.email,
            "first_name": instructor.user.first_name,
            "last_name": instructor.user.last_name,
            "phone": instructor.phone,
            "license_number": instructor.license_number,
            "hire_date": instructor.hire_date,
            "employment_type": instructor.employment_type,
            "hourly_rate": str(instructor.hourly_rate),
            "is_active": instructor.user.is_active,
        }

    @staticmethod
    async def delete_instructor(
        db: AsyncSession,
        user_id: int,
    ):
        instructor = await InstructorRepository.get_by_user_id(
            db,
            user_id,
        )

        if instructor is None:
            raise HTTPException(
                status_code=404,
                detail="Instructor not found.",
            )

        await UserRepository.delete(db, instructor.user)
        await db.commit()

        return {
            "message": "Instructor deleted successfully."
        }

    @staticmethod
    async def get_dashboard(db: AsyncSession):
        return {
            "total_students": await StudentRepository.count_students(db),
            "active_students": await StudentRepository.count_active_students(db),
            "total_instructors": await InstructorRepository.count_instructors(db),
            "active_instructors": await InstructorRepository.count_active_instructors(db),
            "total_users": await UserRepository.count_users(db),
        }