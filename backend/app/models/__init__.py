"""
Data models for the application.
"""

from .base_model import BaseModel
from .employee_model import Employee
from .attendance_model import Attendance

__all__ = ["BaseModel", "Employee", "Attendance"]
