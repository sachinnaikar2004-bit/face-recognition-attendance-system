"""
Application configuration settings.
"""

from typing import List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = Field(default="AI Face Recognition Attendance System", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Database
    mongodb_url: str = Field(..., description="MongoDB connection URL")
    
    # JWT
    jwt_secret: str = Field(..., description="JWT secret key")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=60, description="Access token expiration in minutes")
    refresh_token_expire_days: int = Field(default=7, description="Refresh token expiration in days")
    
    # CORS
    cors_origins: List[str] = Field(default=["http://localhost:5173"], description="CORS allowed origins")
    
    # DeepFace
    deepface_tolerance: float = Field(default=0.6, description="DeepFace verification tolerance")
    max_face_embeddings_per_person: int = Field(default=5, description="Maximum face embeddings per person")
    image_quality_threshold: float = Field(default=0.7, description="Image quality threshold")
    
    # File Upload
    max_file_size: int = Field(default=5242880, description="Maximum file size in bytes")
    allowed_image_types: List[str] = Field(default=["image/jpeg", "image/png"], description="Allowed image types")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, description="Rate limit per minute")
    deepface_rate_limit: int = Field(default=10, description="DeepFace verification rate limit")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
