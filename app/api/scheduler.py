from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import require_scheduler
from app.db.session import get_db
from app.models.user import User
from app.services.scheduler_service import SchedulerService

router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"],
)


@router.get("/profile")
async def get_profile(
    current_scheduler: User = Depends(require_scheduler),
):
    return await SchedulerService.get_profile(current_scheduler)


@router.get("/dashboard")
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_scheduler: User = Depends(require_scheduler),
):
    return await SchedulerService.get_dashboard(db)