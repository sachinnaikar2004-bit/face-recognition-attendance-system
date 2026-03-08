"""
Common response schemas.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SuccessResponse(BaseModel):
    """Schema for successful API responses."""
    success: bool = Field(default=True, description="Success status")
    data: Optional[Any] = Field(None, description="Response data")
    message: str = Field(..., description="Success message")
    timestamp: Optional[datetime] = Field(None, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    success: bool = Field(default=False, description="Success status")
    error: Dict[str, Any] = Field(..., description="Error details")
    timestamp: Optional[datetime] = Field(None, description="Response timestamp")


class PaginationResponse(BaseModel):
    """Schema for pagination information."""
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether next page exists")
    has_prev: bool = Field(..., description="Whether previous page exists")


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    database: str = Field(..., description="Database status")


class FileUploadResponse(BaseModel):
    """Schema for file upload response."""
    success: bool = Field(..., description="Upload success status")
    data: Dict[str, Any] = Field(..., description="Upload data")
    message: str = Field(..., description="Upload message")


class ValidationErrorDetail(BaseModel):
    """Schema for validation error details."""
    field: str = Field(..., description="Field name")
    message: str = Field(..., description="Error message")
    value: Optional[Any] = Field(None, description="Invalid value")


class ValidationErrorResponse(BaseModel):
    """Schema for validation error response."""
    success: bool = Field(default=False, description="Success status")
    error: Dict[str, Any] = Field(..., description="Error details")
    timestamp: Optional[datetime] = Field(None, description="Response timestamp")
