from pydantic import BaseModel


class CourseModuleCreate(BaseModel):
    course_id: int
    title: str
    description: str | None = None
    order_number: int


class CourseModuleUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    order_number: int | None = None


class CourseModuleResponse(BaseModel):
    id: int
    course_id: int
    title: str
    description: str | None
    order_number: int

    model_config = {"from_attributes": True}