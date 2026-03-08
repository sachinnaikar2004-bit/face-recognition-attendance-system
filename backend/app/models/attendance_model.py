"""
Attendance data model.
"""

from datetime import datetime, date
from typing import Optional
from pydantic import Field, validator
from app.models.base_model import BaseDocument


class Attendance(BaseDocument):
    """Attendance model."""
    
    emp_id: str = Field(..., description="Employee ID")
    attendance_date: date = Field(..., description="Attendance date")
    login_time: Optional[str] = Field(None, description="Login time (HH:MM:SS)")
    logout_time: Optional[str] = Field(None, description="Logout time (HH:MM:SS)")
    total_hours: Optional[float] = Field(None, description="Total work hours")
    status: str = Field(default="present", description="Attendance status")
    
    @validator("status")
    def validate_status(cls, v):
        """Validate attendance status."""
        allowed_statuses = ["present", "absent", "half_day", "leave", "holiday"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v
    
    @validator("login_time", "logout_time")
    def validate_time_format(cls, v):
        """Validate time format."""
        if v:
            try:
                datetime.strptime(v, "%H:%M:%S")
            except ValueError:
                raise ValueError("Time must be in HH:MM:SS format")
        return v
    
    @validator("total_hours")
    def validate_total_hours(cls, v):
        """Validate total hours."""
        if v is not None and (v < 0 or v > 24):
            raise ValueError("Total hours must be between 0 and 24")
        return v
    
    class Config:
        collection_name = "attendance"
        indexes = [
            {"keys": [("emp_id", 1), ("date", -1)]},
            {"keys": [("date", -1)]},
            {"keys": [("login_time", -1)]},
            {"keys": [("created_at", -1)]},
        ]
    
    def mark_login(self, login_time: str = None):
        """Mark login time."""
        if login_time:
            self.login_time = login_time
        else:
            self.login_time = datetime.utcnow().strftime("%H:%M:%S")
        self.status = "present"
        self.updated_at = datetime.utcnow()
    
    def mark_logout(self, logout_time: str = None):
        """Mark logout time and calculate total hours."""
        if logout_time:
            self.logout_time = logout_time
        else:
            self.logout_time = datetime.utcnow().strftime("%H:%M:%S")
        
        # Calculate total hours if both login and logout times are present
        if self.login_time and self.logout_time:
            self.total_hours = self._calculate_hours()
        
        self.updated_at = datetime.utcnow()
    
    def _calculate_hours(self) -> float:
        """Calculate total work hours."""
        if not self.login_time or not self.logout_time:
            return 0.0
        
        try:
            login_dt = datetime.strptime(self.login_time, "%H:%M:%S")
            logout_dt = datetime.strptime(self.logout_time, "%H:%M:%S")
            
            # Handle overnight shifts
            if logout_dt < login_dt:
                logout_dt = logout_dt.replace(day=logout_dt.day + 1)
            
            diff = logout_dt - login_dt
            return round(diff.total_seconds() / 3600, 2)
        
        except ValueError:
            return 0.0
    
    def is_active_session(self) -> bool:
        """Check if attendance session is active (logged in but not logged out)."""
        return self.login_time is not None and self.logout_time is None
    
    def get_duration(self) -> Optional[str]:
        """Get formatted duration string."""
        if not self.total_hours:
            return None
        
        hours = int(self.total_hours)
        minutes = int((self.total_hours - hours) * 60)
        
        if hours == 0:
            return f"{minutes}m"
        elif minutes == 0:
            return f"{hours}h"
        else:
            return f"{hours}h {minutes}m"
