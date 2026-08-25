from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.student_enrollment import EnrollmentResponse
from app.services.student_enrollment_service import (
    StudentEnrollmentService,
)

router = APIRouter(
    tags=["Student Enrollments"],
)


@router.get(
    "/students/{student_id}/enrollments",
    response_model=list[EnrollmentResponse],
)
async def get_student_enrollments(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await StudentEnrollmentService.get_student_enrollments(
        db,
        student_id,
    )