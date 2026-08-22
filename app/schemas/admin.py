from pydantic import BaseModel, EmailStr


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