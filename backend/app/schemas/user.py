# backend/app/schemas/user.py - Updated to include name field
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER"
    REPORTER = "REPORTER"

# Input for registration
class UserCreate(BaseModel):
    name: Optional[str] = None
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
    name: Optional[str]
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Returned by login/register API
class Token(BaseModel):
    access_token: str
    token_type: str