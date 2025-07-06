# backend/app/api/auth.py - Make sure this is correct
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, Token, UserOut
from app.services import user_service
from app.core.security import create_access_token
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

# IMPORTANT: This should NOT have prefix="/api/auth" since we add prefix in main.py
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    print(f"📝 Registration attempt for: {user_data.email}")
    
    existing_user = user_service.get_user_by_email(db, user_data.email)
    if existing_user:
        print(f"❌ User already exists: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        new_user = user_service.create_user(db, user_data)
        access_token = create_access_token(data={"sub": new_user.email})
        print(f"✅ User registered successfully: {user_data.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user."""
    print(f"🔐 Login attempt for: {form_data.username}")
    
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        print(f"❌ Invalid credentials for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    print(f"✅ Login successful for: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user