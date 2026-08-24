from pydantic import BaseModel, ConfigDict


class LanguageCreate(BaseModel):
    name: str
    code: str


class LanguageUpdate(BaseModel):
    name: str
    code: str
    is_active: bool


class LanguageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    is_active: bool