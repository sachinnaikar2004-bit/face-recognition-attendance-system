"""
Authentication-related Pydantic schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema for login request."""
    face_image: str = Field(..., description="Base64 encoded face image")


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str = Field(..., description="Refresh token")


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field(..., description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")


class LoginResponse(BaseModel):
    """Schema for login response."""
    success: bool = Field(..., description="Login success status")
    data: dict = Field(..., description="Login data")
    message: str = Field(..., description="Login message")


class UserInfo(BaseModel):
    """Schema for user information."""
    emp_id: str = Field(..., description="Employee ID")
    name: str = Field(..., description="Employee name")
    role: str = Field(..., description="Employee role")
    email: str = Field(..., description="Employee email")
    department: Optional[str] = Field(None, description="Department")


class FaceRecognitionResponse(BaseModel):
    """Schema for face recognition response."""
    verified: bool = Field(..., description="Face verification status")
    emp_id: Optional[str] = Field(None, description="Employee ID if verified")
    name: Optional[str] = Field(None, description="Employee name if verified")
    confidence: Optional[float] = Field(None, description="Recognition confidence")
    message: str = Field(..., description="Response message")


class FaceLoginResponse(BaseModel):
    """Schema for face login response."""
    success: bool = Field(..., description="Login success status")
    data: dict = Field(..., description="Login data including tokens and user info")
    message: str = Field(..., description="Login message")


class FaceLogoutResponse(BaseModel):
    """Schema for face logout response."""
    success: bool = Field(..., description="Logout success status")
    data: dict = Field(..., description="Logout data")
    message: str = Field(..., description="Logout message")


class FaceRegisterRequest(BaseModel):
    """Schema for face registration request."""
    emp_id: str = Field(..., description="Employee ID")
    face_images: list[str] = Field(..., min_items=1, max_items=5, description="Face images for registration")


class FaceRegisterResponse(BaseModel):
    """Schema for face registration response."""
    success: bool = Field(..., description="Registration success status")
    data: dict = Field(..., description="Registration data")
    message: str = Field(..., description="Registration message")
