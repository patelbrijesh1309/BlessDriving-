from datetime import time

from pydantic import BaseModel, ConfigDict


class SchoolSettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    school_name: str
    opening_time: time
    closing_time: time
    default_lesson_duration: int
    buffer_minutes: int
    cancellation_hours: int
    timezone: str


class SchoolSettingUpdate(BaseModel):
    school_name: str
    opening_time: time
    closing_time: time
    default_lesson_duration: int
    buffer_minutes: int
    cancellation_hours: int
    timezone: str