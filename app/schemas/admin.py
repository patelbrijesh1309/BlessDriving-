from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr


# ===================== COMMON USER =====================

class AdminCreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str


class AdminUserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    is_active: bool


# ===================== STUDENT =====================

class AdminCreateStudentRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    phone: str
    date_of_birth: date
    address: str
    pickup_address: Optional[str] = None
    emergency_contact: Optional[str] = None
    notes: Optional[str] = None


class AdminUpdateStudentRequest(BaseModel):
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    pickup_address: Optional[str] = None
    emergency_contact: Optional[str] = None
    notes: Optional[str] = None


# ===================== INSTRUCTOR =====================

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


class AdminUpdateInstructorRequest(BaseModel):
    phone: Optional[str] = None
    license_number: Optional[str] = None
    hire_date: Optional[date] = None
    employment_type: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    is_active: Optional[bool] = None