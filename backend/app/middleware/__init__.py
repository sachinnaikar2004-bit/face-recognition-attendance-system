"""
Middleware components for the application.
"""

from .cors_middleware import setup_cors
from .logging_middleware import setup_logging

__all__ = ["setup_cors", "setup_logging"]
