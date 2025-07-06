# backend/app/schemas/issue.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum
from datetime import datetime

class IssueStatus(str, Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class IssueSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: IssueSeverity = IssueSeverity.MEDIUM
    tags: Optional[str] = None

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[IssueStatus] = None
    severity: Optional[IssueSeverity] = None
    tags: Optional[str] = None
    assigned_to: Optional[UUID] = None

class IssueOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: IssueStatus
    severity: IssueSeverity
    file_path: Optional[str]
    tags: Optional[str]
    created_by: UUID
    assigned_to: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IssueFilter(BaseModel):
    status: Optional[IssueStatus] = None
    severity: Optional[IssueSeverity] = None
    assigned_to: Optional[UUID] = None
    created_by: Optional[UUID] = None