# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from app.api import auth, issue, websocket
from app.worker.scheduler import start_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Issues & Insights Tracker...")
    
    # Start background scheduler
    start_scheduler()
    logger.info("Background scheduler started")
    
    # Create uploads directory
    os.makedirs("uploads", exist_ok=True)
    logger.info("Upload directory ensured")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Issues & Insights Tracker...")

# Create FastAPI app
app = FastAPI(
    title="Issues & Insights Tracker",
    description="A comprehensive issue tracking system with real-time updates",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for file uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(issue.router, prefix="/api")
app.include_router(websocket.router)

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Issues & Insights Tracker API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "websocket": "/ws",
        "status": "operational"
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "issues-insights-tracker"}

@app.get("/api/config")
def get_config():
    """Get frontend configuration."""
    return {
        "websocket_url": "ws://localhost:8000/ws",
        "upload_max_size": 10 * 1024 * 1024,  # 10MB
        "supported_file_types": [
            "image/jpeg", "image/png", "image/gif",
            "application/pdf", "text/plain", "text/csv"
        ]
    }

# Add custom exception handlers
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "http_error"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "type": "validation_error"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "server_error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )