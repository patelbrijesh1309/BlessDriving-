from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleRepository:

    @staticmethod
    async def create(
        db: AsyncSession,
        data: VehicleCreate,
    ) -> Vehicle:

        vehicle = Vehicle(**data.model_dump())

        db.add(vehicle)
        await db.commit()
        await db.refresh(vehicle)

        return vehicle

    @staticmethod
    async def get_all(db: AsyncSession):

        result = await db.execute(
            select(Vehicle).order_by(Vehicle.id)
        )

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        vehicle_id: int,
    ):

        result = await db.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_vehicle_number(
        db: AsyncSession,
        vehicle_number: str,
    ):

        result = await db.execute(
            select(Vehicle).where(
                Vehicle.vehicle_number == vehicle_number
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_plate(
        db: AsyncSession,
        plate: str,
    ):

        result = await db.execute(
            select(Vehicle).where(
                Vehicle.plate == plate
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update(
        db: AsyncSession,
        vehicle: Vehicle,
        data: VehicleUpdate,
    ):

        values = data.model_dump(exclude_unset=True)

        for key, value in values.items():
            setattr(vehicle, key, value)

        await db.commit()
        await db.refresh(vehicle)

        return vehicle

    @staticmethod
    async def delete(
        db: AsyncSession,
        vehicle: Vehicle,
    ):

        await db.delete(vehicle)
        await db.commit()