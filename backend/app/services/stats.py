# backend/app/services/stats.py

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.db.session import SessionLocal
from app.models.issue import Issue, IssueStatus, IssueSeverity
from app.models.daily_stats import DailyStats
from datetime import date, datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def update_stats():
    """Background job to update daily statistics."""
    
    db = SessionLocal()
    try:
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        logger.info(f"Updating daily stats for {today}")
        
        # Get or create daily stats record
        daily_stats = db.query(DailyStats).filter(DailyStats.date == today).first()
        if not daily_stats:
            daily_stats = DailyStats(date=today)
            db.add(daily_stats)
        
        # Count issues by status
        status_counts = db.query(
            Issue.status,
            func.count(Issue.id).label('count')
        ).group_by(Issue.status).all()
        
        # Update status counts
        for status, count in status_counts:
            if status == IssueStatus.OPEN:
                daily_stats.open_count = count
            elif status == IssueStatus.TRIAGED:
                daily_stats.triaged_count = count
            elif status == IssueStatus.IN_PROGRESS:
                daily_stats.in_progress_count = count
            elif status == IssueStatus.DONE:
                daily_stats.done_count = count
        
        # Count issues by severity
        severity_counts = db.query(
            Issue.severity,
            func.count(Issue.id).label('count')
        ).group_by(Issue.severity).all()
        
        # Update severity counts
        for severity, count in severity_counts:
            if severity == IssueSeverity.LOW:
                daily_stats.low_count = count
            elif severity == IssueSeverity.MEDIUM:
                daily_stats.medium_count = count
            elif severity == IssueSeverity.HIGH:
                daily_stats.high_count = count
            elif severity == IssueSeverity.CRITICAL:
                daily_stats.critical_count = count
        
        # Total issues
        daily_stats.total_issues = db.query(Issue).count()
        
        # Issues created today
        daily_stats.issues_created_today = db.query(Issue).filter(
            func.date(Issue.created_at) == today
        ).count()
        
        # Issues closed today (status changed to DONE today)
        daily_stats.issues_closed_today = db.query(Issue).filter(
            and_(
                Issue.status == IssueStatus.DONE,
                func.date(Issue.updated_at) == today
            )
        ).count()
        
        db.commit()
        logger.info(f"Daily stats updated successfully for {today}")
        
        return {
            "date": today,
            "total_issues": daily_stats.total_issues,
            "created_today": daily_stats.issues_created_today,
            "closed_today": daily_stats.issues_closed_today
        }
        
    except Exception as e:
        logger.error(f"Error updating daily stats: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def get_historical_stats(days: int = 30):
    """Get historical statistics for the last N days."""
    
    db = SessionLocal()
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        stats = db.query(DailyStats).filter(
            and_(
                DailyStats.date >= start_date,
                DailyStats.date <= end_date
            )
        ).order_by(DailyStats.date.desc()).all()
        
        return [
            {
                "date": stat.date.isoformat(),
                "total_issues": stat.total_issues,
                "open_count": stat.open_count,
                "triaged_count": stat.triaged_count,
                "in_progress_count": stat.in_progress_count,
                "done_count": stat.done_count,
                "created_today": stat.issues_created_today,
                "closed_today": stat.issues_closed_today
            }
            for stat in stats
        ]
        
    except Exception as e:
        logger.error(f"Error getting historical stats: {e}")
        raise
    finally:
        db.close()