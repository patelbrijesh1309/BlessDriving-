from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.student import (
    StudentRegisterRequest,
    StudentRegisterResponse,
)
from app.schemas.student_language import StudentLanguagesUpdateRequest
from app.services.student_language_service import StudentLanguageService
from app.services.student_service import StudentService

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post("/register", response_model=StudentRegisterResponse)
async def register_student(
    data: StudentRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    return await StudentService.register_student(db, data)


@router.put("/me/languages")
async def update_my_languages(
    request: StudentLanguagesUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await StudentLanguageService.update_languages(
        db,
        current_user.id,
        request.language_ids,
        request.primary_language_id,
    )


@router.get("/me/languages")
async def get_my_languages(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await StudentLanguageService.get_languages(
        db,
        current_user.id,
    )