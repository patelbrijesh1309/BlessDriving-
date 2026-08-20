from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
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