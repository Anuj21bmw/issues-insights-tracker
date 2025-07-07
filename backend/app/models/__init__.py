# backend/app/models/__init__.py

# Import all models here for Alembic autogenerate
from app.models.user import User
from app.models.issue import Issue, IssueStatus, IssueSeverity

__all__ = ["User", "Issue", "IssueStatus", "IssueSeverity"]