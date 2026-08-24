from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)

from app.core.dependencies import get_current_user
from app.schemas.student_language import (
    StudentLanguagesUpdateRequest,
)
from app.services.student_language_service import StudentLanguageService

from app.services.student_service import StudentService

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post("", response_model=StudentResponse)
async def create_student(
    data: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await StudentService.create_student(db, data)


@router.get("", response_model=list[StudentResponse])
async def get_students(
    db: AsyncSession = Depends(get_db),
):
    return await StudentService.get_students(db)


@router.get("/{user_id}", response_model=StudentResponse)
async def get_student(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await StudentService.get_student(db, user_id)


@router.put("/{user_id}", response_model=StudentResponse)
async def update_student(
    user_id: int,
    data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await StudentService.update_student(db, user_id, data)


@router.delete("/{user_id}")
async def delete_student(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await StudentService.delete_student(db, user_id)

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