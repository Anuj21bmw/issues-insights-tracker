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
    """Get dashboard statistics including issue counts by status"""
    
    # Get status breakdown
    status_breakdown = (
        db.query(Issue.status, func.count(Issue.id).label('count'))
        .group_by(Issue.status)
        .all()
    )
    
    # Convert to the format expected by frontend
    status_data = [
        {"status": status.value, "count": count} 
        for status, count in status_breakdown
    ]
    
    # For severity, we'll create mock data since your model doesn't have severity
    # You can add a severity field to your Issue model later
    severity_data = [
        {"severity": "LOW", "count": 0},
        {"severity": "MEDIUM", "count": 0}, 
        {"severity": "HIGH", "count": 0},
        {"severity": "CRITICAL", "count": 0}
    ]
    
    # Get total open issues
    total_open = db.query(Issue).filter(Issue.status == IssueStatus.OPEN).count()
    
    return {
        "status_breakdown": status_data,
        "severity_breakdown": severity_data,
        "total_open": total_open
    }