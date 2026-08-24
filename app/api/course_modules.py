from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.course_module import CourseModuleResponse
from app.services.course_module_service import CourseModuleService

router = APIRouter(
    tags=["Course Modules"],
)


@router.get(
    "/courses/{course_id}/modules",
    response_model=list[CourseModuleResponse],
)
async def get_course_modules(
    course_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await CourseModuleService.get_course_modules(
        db,
        course_id,
    )


@router.get(
    "/course-modules/{module_id}",
    response_model=CourseModuleResponse,
)
async def get_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await CourseModuleService.get_module(
        db,
        module_id,
    )