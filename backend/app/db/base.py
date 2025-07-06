from app.db.base_class import Base

# Import models here for Alembic autogenerate, but don't import user in issue model
from app.models.user import User  # Keep this
from app.models.issue import Issue  # Keep this

# Define lazy import function for Alembic autogenerate
def import_models():
    """Import all models for Alembic autogenerate"""
    pass  