from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    description: str | None = None
    duration_hours: int
    price: float


class CourseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    duration_hours: int | None = None
    price: float | None = None
    is_active: bool | None = None


class CourseResponse(BaseModel):
    id: int
    name: str
    description: str | None
    duration_hours: int
    price: float
    is_active: bool

    model_config = {"from_attributes": True}