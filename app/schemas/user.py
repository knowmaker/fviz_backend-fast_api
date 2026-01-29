# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class ConfirmRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    email: EmailStr
    last_name: str | None = None
    first_name: str | None = None
    patronymic: str | None = None
    is_confirmed: bool
    is_admin: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    last_name: str | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=255)
    patronymic: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=6, max_length=128)
