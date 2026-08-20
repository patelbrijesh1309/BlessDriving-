from datetime import date

from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    user_id: int
    phone: str
    date_of_birth: date
    address: str
    pickup_address: str | None = None
    emergency_contact: str | None = None
    notes: str | None = None


class StudentUpdate(BaseModel):
    phone: str | None = None
    date_of_birth: date | None = None
    address: str | None = None
    pickup_address: str | None = None
    emergency_contact: str | None = None
    notes: str | None = None


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    phone: str
    date_of_birth: date
    address: str
    pickup_address: str | None
    emergency_contact: str | None
    notes: str | None