"""
API routers for the application.
"""

from .employee_router import router as employee_router
from .attendance_router import router as attendance_router
from .face_router import router as face_router
from .auth_router import router as auth_router

__all__ = ["employee_router", "attendance_router", "face_router", "auth_router"]
