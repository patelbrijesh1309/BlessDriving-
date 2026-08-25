from datetime import date

from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentUpdate(BaseModel):
    status: str


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: date
    status: str

    model_config = {"from_attributes": True}