from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class InstructorCreate(BaseModel):
    user_id: int
    phone: str
    license_number: str
    hire_date: date
    employment_type: str
    hourly_rate: Decimal


class InstructorUpdate(BaseModel):
    phone: str | None = None
    license_number: str | None = None
    hire_date: date | None = None
    employment_type: str | None = None
    hourly_rate: Decimal | None = None
    is_active: bool | None = None


class InstructorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    phone: str
    license_number: str
    hire_date: date
    employment_type: str
    hourly_rate: Decimal
    is_active: bool