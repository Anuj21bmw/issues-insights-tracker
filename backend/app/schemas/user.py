# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from uuid import UUID

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER"
    REPORTER = "REPORTER"

# Input for registration
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.REPORTER

# Input for manual login (if not using OAuth2PasswordRequestForm)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Output schema (used in /me response)
class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True  # Use this for Pydantic v2

# Returned by login/register API
class Token(BaseModel):
    access_token: str
    token_type: str