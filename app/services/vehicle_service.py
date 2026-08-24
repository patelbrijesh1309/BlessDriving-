from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleService:

    @staticmethod
    async def create_vehicle(
        db: AsyncSession,
        data: VehicleCreate,
    ):

        if await VehicleRepository.get_by_vehicle_number(
            db,
            data.vehicle_number,
        ):
            raise HTTPException(
                status_code=400,
                detail="Vehicle number already exists.",
            )

        if await VehicleRepository.get_by_plate(
            db,
            data.plate,
        ):
            raise HTTPException(
                status_code=400,
                detail="Plate already exists.",
            )

        return await VehicleRepository.create(db, data)

    @staticmethod
    async def get_vehicles(db: AsyncSession):

        return await VehicleRepository.get_all(db)

    @staticmethod
    async def get_vehicle(
        db: AsyncSession,
        vehicle_id: int,
    ):

        vehicle = await VehicleRepository.get_by_id(
            db,
            vehicle_id,
        )

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail="Vehicle not found.",
            )

        return vehicle

    @staticmethod
    async def update_vehicle(
        db: AsyncSession,
        vehicle_id: int,
        data: VehicleUpdate,
    ):

        vehicle = await VehicleRepository.get_by_id(
            db,
            vehicle_id,
        )

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail="Vehicle not found.",
            )

        return await VehicleRepository.update(
            db,
            vehicle,
            data,
        )

    @staticmethod
    async def delete_vehicle(
        db: AsyncSession,
        vehicle_id: int,
    ):

        vehicle = await VehicleRepository.get_by_id(
            db,
            vehicle_id,
        )

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail="Vehicle not found.",
            )

        await VehicleRepository.delete(
            db,
            vehicle,
        )

        return {"message": "Vehicle deleted successfully."}