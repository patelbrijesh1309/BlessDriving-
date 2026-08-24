from pydantic import BaseModel


class VehicleCreate(BaseModel):
    vehicle_number: str
    make: str
    model: str
    plate: str
    transmission: str


class VehicleUpdate(BaseModel):
    vehicle_number: str
    make: str
    model: str
    plate: str
    transmission: str
    is_active: bool


class VehicleResponse(BaseModel):
    id: int
    vehicle_number: str
    make: str
    model: str
    plate: str
    transmission: str
    is_active: bool

    model_config = {"from_attributes": True}