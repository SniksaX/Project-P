from uuid import uuid4, UUID
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class TokenRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[UUID] = None


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value


class User(UserBase):
    id: UUID = Field(default_factory=uuid4)
    is_verified: bool = False
    verification_token: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class MovieBase(BaseModel):
    title: str
    description: str | None = None
    rating: int = Field(..., ge=1, le=100)
    release_date: date
    tmdb_id: int | None = None


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    created_at: datetime
