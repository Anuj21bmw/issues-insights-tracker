# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
