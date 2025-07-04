# backend/app/db/base.py

from app.db.base_class import Base

# Define lazy import function for Alembic autogenerate
def import_models():
    from app.models import user  # ✅ Only used when explicitly called
