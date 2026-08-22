from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


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
    user_id: int
    phone: str
    license_number: str
    hire_date: date
    employment_type: str
    hourly_rate: Decimal
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class AdminCreateInstructorRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    phone: str
    license_number: str
    hire_date: date
    employment_type: str
    hourly_rate: Decimal

class AdminInstructorItem(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    license_number: Optional[str] = None
    hire_date: Optional[date] = None
    employment_type: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    is_active: bool


class AdminInstructorListResponse(BaseModel):
    items: list[AdminInstructorItem]
    total: int
    page: int
    limit: int