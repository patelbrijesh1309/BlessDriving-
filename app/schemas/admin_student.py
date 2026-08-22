from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


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


class AdminStudentResponse(BaseModel):
    user_id: int

    email: EmailStr
    first_name: str
    last_name: str

    role: str

    phone: str
    date_of_birth: date
    address: str
    pickup_address: Optional[str] = None
    emergency_contact: Optional[str] = None
    notes: Optional[str] = None

    is_active: bool


class AdminStudentItem(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    pickup_address: Optional[str] = None
    emergency_contact: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool


class AdminStudentListResponse(BaseModel):
    items: list[AdminStudentItem]
    total: int
    page: int
    limit: int

class AdminUpdateStudentRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    pickup_address: Optional[str] = None
    emergency_contact: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None