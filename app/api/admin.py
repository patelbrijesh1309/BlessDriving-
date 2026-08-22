from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from app.core.permissions import require_admin
from app.db.session import get_db
from app.models.user import User
from fastapi import Query
from app.schemas.admin_student import AdminStudentListResponse

from app.schemas.admin import (
    AdminCreateUserRequest,
    AdminUserResponse,
)
from app.schemas.instructor import (
    AdminCreateInstructorRequest,
    AdminInstructorListResponse,
)

from app.schemas.admin_student import (
    AdminCreateStudentRequest,
    AdminStudentResponse,
    AdminStudentListResponse,
    AdminUpdateStudentRequest,
)
from app.schemas.instructor import InstructorUpdate
from app.schemas.instructor import AdminCreateInstructorRequest
from app.services.admin_service import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/users",
    response_model=AdminUserResponse,
)
async def create_user(
    data: AdminCreateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.create_user(db, data)


@router.post(
    "/students",
    response_model=AdminStudentResponse,
)
async def create_student(
    data: AdminCreateStudentRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    print(">>> Student endpoint reached")
    return await AdminService.create_student(db, data)


@router.post(
    "/instructors",
    status_code=201,
)
async def create_instructor(
    data: AdminCreateInstructorRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.create_instructor(db, data)



@router.get(
    "/students",
    response_model=AdminStudentListResponse,
)
async def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.get_students(
        db,
        page,
        limit,
    )

@router.get(
    "/students/{user_id}",
    response_model=AdminStudentResponse,
)
async def get_student_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.get_student_by_id(
        db,
        user_id,
    )


@router.put(
    "/students/{user_id}",
    response_model=AdminStudentResponse,
)
async def update_student(
    user_id: int,
    data: AdminUpdateStudentRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.update_student(
        db,
        user_id,
        data,
    )

@router.delete(
    "/students/{user_id}",
)
async def delete_student(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.delete_student(
        db,
        user_id,
    )

@router.get(
    "/instructors",
    response_model=AdminInstructorListResponse,
)
async def get_instructors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.get_instructors(
        db,
        page,
        limit,
    )

@router.get(
    "/instructors/{user_id}",
)
async def get_instructor(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.get_instructor(
        db,
        user_id,
    )

@router.put(
    "/instructors/{user_id}",
)
async def update_instructor(
    user_id: int,
    data: InstructorUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.update_instructor(
        db,
        user_id,
        data,
    )

@router.delete(
    "/instructors/{user_id}",
)
async def delete_instructor(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.delete_instructor(
        db,
        user_id,
    )

@router.get("/dashboard")
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await AdminService.get_dashboard(db)