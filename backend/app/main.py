"""
Main FastAPI application for AI Face Recognition Attendance System.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.exceptions import (
    CustomException, custom_exception_handler, 
    validation_exception_handler, http_exception_handler, 
    general_exception_handler
)
from app.database.connection import init_database, close_database
from app.routers import (
    employee_router, attendance_router, 
    face_router, auth_router
)
from app.middleware.cors_middleware import setup_cors
from app.middleware.logging_middleware import setup_logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting AI Face Recognition Attendance System...")
    
    try:
        # Initialize database
        await init_database()
        logger.info("Database initialized successfully")
        
        # Load machine learning models
        logger.info("Machine learning models loaded")
        
        yield
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
    
    finally:
        # Shutdown
        logger.info("Shutting down application...")
        await close_database()
        logger.info("Database connection closed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A production-ready face recognition attendance system",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Setup middleware
setup_cors(app)
setup_logging(app)

# Setup exception handlers
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(employee_router, prefix="/api/v1")
app.include_router(attendance_router, prefix="/api/v1")
app.include_router(face_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Face Recognition Attendance System API",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs" if settings.debug else "Documentation disabled in production"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        from database.mongodb import db
        database = db.get_database()
        await database.command('ping')
        
        return {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z",
            "version": settings.app_version,
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "version": settings.app_version,
                "database": "disconnected",
                "error": str(e)
            }
        )


@app.get("/api/v1")
async def api_info():
    """API information endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI Face Recognition Attendance System API",
        "endpoints": {
            "authentication": "/api/v1/auth",
            "employees": "/api/v1/employees",
            "attendance": "/api/v1/attendance",
            "deepface": "/api/v1/face"
        },
        "documentation": "/docs" if settings.debug else "Documentation disabled in production"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
