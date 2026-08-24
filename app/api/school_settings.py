from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import (
    require_admin,
    require_scheduler,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.school_setting import (
    SchoolSettingResponse,
    SchoolSettingUpdate,
)
from app.services.school_setting_service import (
    SchoolSettingService,
)

router = APIRouter(tags=["School Settings"])


@router.get(
    "/admin/settings",
    response_model=SchoolSettingResponse,
)
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await SchoolSettingService.get_settings(db)


@router.put(
    "/admin/settings",
    response_model=SchoolSettingResponse,
)
async def update_settings(
    data: SchoolSettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return await SchoolSettingService.update_settings(
        db,
        data,
    )


@router.get(
    "/scheduler/settings",
    response_model=SchoolSettingResponse,
)
async def scheduler_settings(
    db: AsyncSession = Depends(get_db),
    current_scheduler: User = Depends(require_scheduler),
):
    return await SchoolSettingService.get_settings(db)