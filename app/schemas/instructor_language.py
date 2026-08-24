from pydantic import BaseModel


class InstructorLanguageUpdate(BaseModel):
    language_ids: list[int]
    primary_language_id: int


class InstructorLanguageItem(BaseModel):
    id: int
    name: str
    code: str
    is_primary: bool