"""
Custom exception handlers for the application.
"""

from typing import Union
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class CustomException(Exception):
    """Base custom exception class."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(CustomException):
    """Validation exception."""
    
    def __init__(self, message: str, details: dict = None):
        self.details = details or {}
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class AuthenticationException(CustomException):
    """Authentication exception."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class AuthorizationException(CustomException):
    """Authorization exception."""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class NotFoundException(CustomException):
    """Resource not found exception."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class DuplicateResourceException(CustomException):
    """Duplicate resource exception."""
    
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class FaceRecognitionException(CustomException):
    """Face recognition specific exception."""
    
    def __init__(self, message: str, details: dict = None):
        self.details = details or {}
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class DatabaseException(CustomException):
    """Database operation exception."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    """Handle custom exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.__class__.__name__,
                "message": exc.message,
                "details": getattr(exc, "details", {})
            },
            "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation exceptions."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed",
                "details": exc.errors()
            },
            "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
        }
    )


async def http_exception_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]) -> JSONResponse:
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": {}
            },
            "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": {"detail": str(exc)} if exc else {}
            },
            "timestamp": request.state.timestamp if hasattr(request.state, "timestamp") else None
        }
    )
