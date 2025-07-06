# backend/app/main.py - Fixed version with dashboard router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging
import os

# Import existing routers
from app.api import auth, issue, dashboard

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
    
    # Start background scheduler (optional)
    try:
        from app.workers.scheduler import start_scheduler
        start_scheduler()
        logger.info("Background scheduler started")
    except ImportError:
        logger.info("Background scheduler not available (optional)")
    except Exception as e:
        logger.warning(f"Failed to start background scheduler: {e}")
    
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
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS - Fixed for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:4173",  # Vite preview
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",  # Alternative frontend port
        "*"  # Allow all during development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static files for file uploads (only if directory exists)
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers - FIXED: Include dashboard router
app.include_router(auth.router, prefix="/api")
app.include_router(issue.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Try to include websocket router if it exists
try:
    from app.api import websocket
    app.include_router(websocket.router)
    logger.info("WebSocket router included")
except ImportError:
    logger.info("WebSocket router not available (optional)")

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Issues & Insights Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
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
        "upload_max_size": 10 * 1024 * 1024,  # 10MB
        "supported_file_types": [
            "image/jpeg", "image/png", "image/gif",
            "application/pdf", "text/plain", "text/csv"
        ]
    }

# Custom exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "http_error"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation Error: {exc.errors()}")
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