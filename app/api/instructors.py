from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.instructor import (
    InstructorCreate,
    InstructorResponse,
    InstructorUpdate,
)
from app.services.instructor_service import InstructorService

router = APIRouter(
    prefix="/instructors",
    tags=["Instructors"],
)


@router.post("", response_model=InstructorResponse)
async def create_instructor(
    data: InstructorCreate,
    db: AsyncSession = Depends(get_db),
):
    return await InstructorService.create_instructor(db, data)


@router.get("", response_model=list[InstructorResponse])
async def get_instructors(
    db: AsyncSession = Depends(get_db),
):
    return await InstructorService.get_instructors(db)


@router.get("/{user_id}", response_model=InstructorResponse)
async def get_instructor(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await InstructorService.get_instructor(db, user_id)


@router.put("/{user_id}", response_model=InstructorResponse)
async def update_instructor(
    user_id: int,
    data: InstructorUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await InstructorService.update_instructor(db, user_id, data)


@router.delete("/{user_id}")
async def delete_instructor(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await InstructorService.delete_instructor(db, user_id)