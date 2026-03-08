"""
Dependency injection modules.
"""

from .auth_dependency import get_current_user
from .database_dependency import get_database

__all__ = ["get_current_user", "get_database"]
