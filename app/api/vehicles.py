from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
)
from app.services.vehicle_service import VehicleService

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)


@router.get("", response_model=list[VehicleResponse])
async def get_vehicles(
    db: AsyncSession = Depends(get_db),
):
    return await VehicleService.get_vehicles(db)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await VehicleService.get_vehicle(
        db,
        vehicle_id,
    )