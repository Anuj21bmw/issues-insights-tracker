# backend/app/core/deps.py - Fixed authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User, RoleEnum
from app.core.config import settings

# Define the OAuth2 scheme - FIXED: Correct token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Get the current logged-in user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    print(f"🔍 Authenticating user with token: {token[:20]}...")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        print(f"📧 Token decoded, email: {email}")
        
        if email is None:
            print("❌ No email in token")
            raise credentials_exception
            
    except JWTError as e:
        print(f"❌ JWT decode error: {e}")
        raise credentials_exception

    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        print(f"❌ User not found in database: {email}")
        raise credentials_exception
    
    print(f"✅ User authenticated: {user.email}")
    return user

# WebSocket authentication (doesn't use Depends)
async def get_current_user_websocket(token: str) -> User:
    """Authenticate user for WebSocket connections."""
    from app.db.session import SessionLocal
    
    credentials_exception = Exception("Could not validate credentials")
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()

# Require a specific role (e.g., ADMIN only)
def require_role(required_role: RoleEnum):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: {required_role} role required",
            )
        return current_user
    return role_checker

# Require any of the given roles (e.g., ADMIN or MAINTAINER)
def require_roles(*roles: RoleEnum):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            allowed_roles = ", ".join([r.value for r in roles])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: one of [{allowed_roles}] role required",
            )
        return current_user
    return role_checker