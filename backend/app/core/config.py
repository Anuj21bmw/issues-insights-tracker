# backend/app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional
import secrets

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/tracker"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Issues & Insights Tracker"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, specify exact origins
    
    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = [
        "image/jpeg", "image/png", "image/gif",
        "application/pdf", "text/plain", "text/csv",
        "application/msword", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    # WebSocket Configuration
    WEBSOCKET_PING_INTERVAL: int = 30
    WEBSOCKET_PING_TIMEOUT: int = 10
    
    # Background Jobs Configuration
    STATS_UPDATE_INTERVAL_MINUTES: int = 30
    CLEANUP_INTERVAL_HOURS: int = 24
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    # Email Configuration (for future use)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # OAuth Configuration (for future use)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # Redis Configuration (for future caching)
    REDIS_URL: Optional[str] = None
    
    # Monitoring Configuration
    ENABLE_METRICS: bool = True
    METRICS_PATH: str = "/metrics"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Validate critical settings
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set")
        
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set")

settings = Settings()

# Derived settings
DATABASE_URL_ASYNC = settings.DATABASE_URL.replace(
    "postgresql+psycopg2://", "postgresql+asyncpg://"
)

# Environment-specific configurations
ENVIRONMENT = {
    "development": {
        "debug": True,
        "reload": True,
        "log_level": "DEBUG"
    },
    "production": {
        "debug": False,
        "reload": False,
        "log_level": "INFO"
    }
}