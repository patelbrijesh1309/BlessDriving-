from pydantic import BaseModel


class StudentLanguagesUpdateRequest(BaseModel):
    language_ids: list[int]
    primary_language_id: int


class StudentLanguageResponse(BaseModel):
    id: int
    name: str
    code: str
    is_primary: bool