# backend/app/api/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.issue import Issue, IssueStatus
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get issue counts by status
    total_issues = db.query(Issue).count()
    open_issues = db.query(Issue).filter(Issue.status == IssueStatus.OPEN).count()
    in_progress_issues = db.query(Issue).filter(Issue.status == IssueStatus.IN_PROGRESS).count()
    resolved_issues = db.query(Issue).filter(Issue.status == IssueStatus.RESOLVED).count()
    closed_issues = db.query(Issue).filter(Issue.status == IssueStatus.CLOSED).count()
    
    # Get recent issues (last 5)
    recent_issues = db.query(Issue).order_by(Issue.created_at.desc()).limit(5).all()
    
    return {
        "total_issues": total_issues,
        "open_issues": open_issues,
        "in_progress_issues": in_progress_issues,
        "resolved_issues": resolved_issues,
        "closed_issues": closed_issues,
        "recent_issues": recent_issues
    }