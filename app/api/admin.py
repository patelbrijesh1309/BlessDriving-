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
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
)
from app.services.vehicle_service import VehicleService
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
)
from app.services.course_service import CourseService

from app.schemas.course_module import (
    CourseModuleCreate,
    CourseModuleUpdate,
    CourseModuleResponse,
)
from app.services.course_module_service import CourseModuleService

from app.schemas.instructor import InstructorUpdate
from app.schemas.instructor import AdminCreateInstructorRequest
from app.services.admin_service import AdminService



router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)
from app.schemas.language import (
    LanguageCreate,
    LanguageResponse,
    LanguageUpdate,
)
from app.services.language_service import LanguageService


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

@router.post(
    "/languages",
    response_model=LanguageResponse,
)
async def create_language(
    data: LanguageCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await LanguageService.create_language(
        db,
        data,
    )


@router.get(
    "/languages",
    response_model=list[LanguageResponse],
)
async def get_languages(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await LanguageService.get_languages(db)


@router.get(
    "/languages/{language_id}",
    response_model=LanguageResponse,
)
async def get_language(
    language_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await LanguageService.get_language(
        db,
        language_id,
    )


@router.put(
    "/languages/{language_id}",
    response_model=LanguageResponse,
)
async def update_language(
    language_id: int,
    data: LanguageUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await LanguageService.update_language(
        db,
        language_id,
        data,
    )


@router.delete(
    "/languages/{language_id}",
)
async def delete_language(
    language_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await LanguageService.delete_language(
        db,
        language_id,
    )

@router.post(
    "/vehicles",
    response_model=VehicleResponse,
)
async def create_vehicle(
    data: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await VehicleService.create_vehicle(
        db,
        data,
    )


@router.put(
    "/vehicles/{vehicle_id}",
    response_model=VehicleResponse,
)
async def update_vehicle(
    vehicle_id: int,
    data: VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await VehicleService.update_vehicle(
        db,
        vehicle_id,
        data,
    )


@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await VehicleService.delete_vehicle(
        db,
        vehicle_id,
    )

@router.post(
    "/courses",
    response_model=CourseResponse,
)
async def create_course(
    data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await CourseService.create_course(db, data)


@router.put(
    "/courses/{course_id}",
    response_model=CourseResponse,
)
async def update_course(
    course_id: int,
    data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await CourseService.update_course(db, course_id, data)


@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await CourseService.delete_course(db, course_id)

@router.post(
    "/course-modules",
    response_model=CourseModuleResponse,
)
async def create_course_module(
    data: CourseModuleCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await CourseModuleService.create_module(db, data)


@router.put(
    "/course-modules/{module_id}",
    response_model=CourseModuleResponse,
)
async def update_course_module(
    module_id: int,
    data: CourseModuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await CourseModuleService.update_module(
        db,
        module_id,
        data,
    )


@router.delete("/course-modules/{module_id}")
async def delete_course_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(require_admin),
):
    return await CourseModuleService.delete_module(
        db,
        module_id,
    )