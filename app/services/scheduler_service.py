from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.student_repository import StudentRepository
from app.repositories.instructor_repository import InstructorRepository


class SchedulerService:

    @staticmethod
    async def get_profile(current_user: User):
        return {
            "id": current_user.id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "role": "SCHEDULER",
            "is_active": current_user.is_active,
        }

    @staticmethod
    async def get_dashboard(db: AsyncSession):
        return {
            "total_students": await StudentRepository.count_students(db),
            "active_students": await StudentRepository.count_active_students(db),
            "total_instructors": await InstructorRepository.count_instructors(db),
            "active_instructors": await InstructorRepository.count_active_instructors(db),

            # Future modules
            "today_lessons": 0,
            "pending_lessons": 0,
            "available_vehicles": 0,
            "pending_enrollments": 0,
        }