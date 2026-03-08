"""
Attendance-related Pydantic schemas.
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class AttendanceBase(BaseModel):
    """Base attendance schema."""
    emp_id: str = Field(..., description="Employee ID")
    attendance_date: date = Field(..., description="Attendance date")
    status: str = Field(default="present", description="Attendance status")


class AttendanceCreate(AttendanceBase):
    """Schema for creating attendance record."""
    login_time: Optional[str] = Field(None, description="Login time (HH:MM:SS)")
    logout_time: Optional[str] = Field(None, description="Logout time (HH:MM:SS)")


class AttendanceUpdate(BaseModel):
    """Schema for updating attendance record."""
    login_time: Optional[str] = Field(None, description="Login time (HH:MM:SS)")
    logout_time: Optional[str] = Field(None, description="Logout time (HH:MM:SS)")
    status: Optional[str] = Field(None, description="Attendance status")


class AttendanceResponse(BaseModel):
    """Schema for attendance response."""
    id: str = Field(..., description="Attendance record ID")
    emp_id: str = Field(..., description="Employee ID")
    name: Optional[str] = Field(None, description="Employee name")
    attendance_date: date = Field(..., description="Attendance date")
    login_time: Optional[str] = Field(None, description="Login time")
    logout_time: Optional[str] = Field(None, description="Logout time")
    total_hours: Optional[float] = Field(None, description="Total work hours")
    status: str = Field(..., description="Attendance status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    duration: Optional[str] = Field(None, description="Formatted duration")
    is_active_session: bool = Field(..., description="Whether session is active")
    
    class Config:
        orm_mode = True


class AttendanceListResponse(BaseModel):
    """Schema for attendance list response."""
    attendance: List[AttendanceResponse] = Field(..., description="List of attendance records")
    pagination: dict = Field(..., description="Pagination information")
    summary: Optional[dict] = Field(None, description="Summary statistics")


class AttendanceFilter(BaseModel):
    """Schema for attendance filters."""
    emp_id: Optional[str] = Field(None, description="Filter by employee ID")
    date_from: Optional[date] = Field(None, description="Filter from date")
    date_to: Optional[date] = Field(None, description="Filter to date")
    status: Optional[str] = Field(None, description="Filter by status")
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page")


class TodayAttendanceResponse(BaseModel):
    """Schema for today's attendance response."""
    attendance_date: date = Field(..., description="Today's date")
    records: List[AttendanceResponse] = Field(..., description="Today's attendance records")
    summary: dict = Field(..., description="Summary statistics")


class AttendanceStatsResponse(BaseModel):
    """Schema for attendance statistics."""
    period: str = Field(..., description="Statistics period")
    total_employees: int = Field(..., description="Total number of employees")
    present_today: int = Field(..., description="Number present today")
    absent_today: int = Field(..., description="Number absent today")
    average_attendance_rate: float = Field(..., description="Average attendance rate")
    daily_breakdown: List[dict] = Field(..., description="Daily breakdown")
    department_breakdown: List[dict] = Field(..., description="Department breakdown")


class EmployeeAttendanceHistory(BaseModel):
    """Schema for employee attendance history."""
    emp_id: str = Field(..., description="Employee ID")
    name: str = Field(..., description="Employee name")
    records: List[AttendanceResponse] = Field(..., description="Attendance records")
    summary: dict = Field(..., description="Summary statistics")
