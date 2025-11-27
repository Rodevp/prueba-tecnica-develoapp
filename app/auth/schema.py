from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(..., example="Juan Pérez")
    email: EmailStr = Field(..., example="juan@mail.com")
    password: str = Field(..., min_length=6, example="123456")
    role_name: str = Field(..., example="user | admin")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="juan@mail.com")
    password: str = Field(..., min_length=6, example="123456")


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., example="juan@mail.com")


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., example="eyJhbGciOi...")
    new_password: str = Field(..., min_length=6, example="newpass123")


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
