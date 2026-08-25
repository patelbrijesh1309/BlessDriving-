from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import require_instructor
from app.db.session import get_db
from app.models.user import User
from app.schemas.instructor_language import (
    InstructorLanguageItem,
    InstructorLanguageUpdate,
)
from app.services.instructor_language_service import (
    InstructorLanguageService,
)

router = APIRouter(
    prefix="/instructors",
    tags=["Instructors"],
)


@router.get(
    "/me/languages",
    response_model=list[InstructorLanguageItem],
)
async def get_my_languages(
    db: AsyncSession = Depends(get_db),
    current_instructor: User = Depends(require_instructor),
):
    return await InstructorLanguageService.get_my_languages(
        db,
        current_instructor.id,
    )


@router.put(
    "/me/languages",
    response_model=list[InstructorLanguageItem],
)
async def update_my_languages(
    data: InstructorLanguageUpdate,
    db: AsyncSession = Depends(get_db),
    current_instructor: User = Depends(require_instructor),
):
    return await InstructorLanguageService.update_my_languages(
        db,
        current_instructor.id,
        data,
    )