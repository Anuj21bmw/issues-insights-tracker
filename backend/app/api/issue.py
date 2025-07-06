# backend/app/api/issue.py

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path

from app.db.session import get_db
from app.models.issue import Issue, IssueStatus, IssueSeverity
from app.schemas.issue import IssueCreate, IssueUpdate, IssueOut, IssueFilter
from app.core.deps import get_current_user, require_roles
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/issues", tags=["issues"])

# Create upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/", response_model=IssueOut)
async def create_issue(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    severity: IssueSeverity = Form(IssueSeverity.MEDIUM),
    tags: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new issue with optional file upload."""
    
    file_path = None
    if file:
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_path = str(file_path)
    
    new_issue = Issue(
        title=title,
        description=description,
        severity=severity,
        tags=tags,
        file_path=file_path,
        created_by=current_user.id
    )
    
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

@router.get("/", response_model=List[IssueOut])
def list_issues(
    status: Optional[IssueStatus] = Query(None),
    severity: Optional[IssueSeverity] = Query(None),
    assigned_to: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List issues with filtering. REPORTER sees only their issues."""
    
    query = db.query(Issue)
    
    # Role-based filtering
    if current_user.role == RoleEnum.REPORTER:
        query = query.filter(Issue.created_by == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Issue.status == status)
    if severity:
        query = query.filter(Issue.severity == severity)
    if assigned_to:
        query = query.filter(Issue.assigned_to == assigned_to)
    
    return query.order_by(Issue.created_at.desc()).all()

@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(
    issue_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get issue by ID with role-based access control."""
    
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # REPORTER can only see their own issues
    if current_user.role == RoleEnum.REPORTER and issue.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return issue

@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(
    issue_id: str,
    update: IssueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update issue. MAINTAINER+ can update any issue, REPORTER only their own."""
    
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # REPORTER can only update their own issues and limited fields
    if current_user.role == RoleEnum.REPORTER:
        if issue.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        # REPORTERs can only update title, description, severity
        allowed_fields = {"title", "description", "severity", "tags"}
        update_dict = update.dict(exclude_unset=True)
        update_dict = {k: v for k, v in update_dict.items() if k in allowed_fields}
    else:
        # MAINTAINER+ can update all fields
        update_dict = update.dict(exclude_unset=True)
    
    for field, value in update_dict.items():
        setattr(issue, field, value)
    
    db.commit()
    db.refresh(issue)
    return issue

@router.delete("/{issue_id}")
def delete_issue(
    issue_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(RoleEnum.ADMIN))  # Only ADMIN can delete
):
    """Delete issue (ADMIN only)."""
    
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Delete associated file if exists
    if issue.file_path and os.path.exists(issue.file_path):
        os.remove(issue.file_path)
    
    db.delete(issue)
    db.commit()
    return {"message": "Issue deleted successfully"}

@router.get("/stats/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(RoleEnum.MAINTAINER, RoleEnum.ADMIN))
):
    """Get dashboard statistics for charts."""
    
    # Issues by severity
    severity_stats = db.query(
        Issue.severity,
        db.func.count(Issue.id).label('count')
    ).filter(
        Issue.status.in_([IssueStatus.OPEN, IssueStatus.TRIAGED, IssueStatus.IN_PROGRESS])
    ).group_by(Issue.severity).all()
    
    # Issues by status
    status_stats = db.query(
        Issue.status,
        db.func.count(Issue.id).label('count')
    ).group_by(Issue.status).all()
    
    return {
        "severity_breakdown": [{"severity": s.severity, "count": s.count} for s in severity_stats],
        "status_breakdown": [{"status": s.status, "count": s.count} for s in status_stats],
        "total_open": sum(s.count for s in severity_stats)
    }