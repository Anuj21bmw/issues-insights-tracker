# backend/app/db/base.py
from app.db.base_class import Base


# The models will be imported by Alembic when needed
__all__ = ["Base"]