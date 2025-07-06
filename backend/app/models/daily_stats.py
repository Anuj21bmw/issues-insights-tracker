# backend/app/models/daily_stats.py

from sqlalchemy import Column, Integer, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from app.models.issue import IssueStatus, IssueSeverity
from datetime import date
import uuid

class DailyStats(Base):
    __tablename__ = "daily_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False, unique=True)
    
    # Status counts
    open_count = Column(Integer, default=0)
    triaged_count = Column(Integer, default=0)
    in_progress_count = Column(Integer, default=0)
    done_count = Column(Integer, default=0)
    
    # Severity counts
    low_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    
    # Totals
    total_issues = Column(Integer, default=0)
    issues_created_today = Column(Integer, default=0)
    issues_closed_today = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<DailyStats(date={self.date}, total={self.total_issues})>"