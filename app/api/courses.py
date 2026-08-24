from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.course import CourseResponse
from app.services.course_service import CourseService

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.get("", response_model=list[CourseResponse])
async def get_courses(
    db: AsyncSession = Depends(get_db),
):
    return await CourseService.get_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await CourseService.get_course(db, course_id)