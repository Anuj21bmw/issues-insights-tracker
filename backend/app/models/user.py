# backend/app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime
import uuid
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER" 
    REPORTER = "REPORTER"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.REPORTER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to issues
    issues = relationship("Issue", back_populates="creator")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"