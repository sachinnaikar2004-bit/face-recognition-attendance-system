"""
Employee-related Pydantic schemas.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    """Base employee schema."""
    name: str = Field(..., min_length=2, max_length=100, description="Employee name")
    email: EmailStr = Field(..., description="Employee email")
    role: str = Field(default="employee", description="Employee role")
    department_name: Optional[str] = Field(None, description="Department")


class EmployeeCreate(EmployeeBase):
    """Schema for creating employee."""
    emp_id: str = Field(..., description="Employee ID")
    face_image: Optional[str] = Field(None, description="Base64 encoded face image")


class EmployeeUpdate(BaseModel):
    """Schema for updating employee."""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Employee name")
    email: Optional[EmailStr] = Field(None, description="Employee email")
    role: Optional[str] = Field(None, description="Employee role")
    department_name: Optional[str] = Field(None, description="Department")
    face_image: Optional[str] = Field(None, description="Base64 encoded face image")


class EmployeeResponse(EmployeeBase):
    """Schema for employee response."""
    id: str = Field(..., description="Employee ID")
    emp_id: str = Field(..., description="Employee ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    is_active: bool = Field(..., description="Employee active status")
    has_face_encoding: bool = Field(..., description="Whether employee has face encoding")
    
    class Config:
        orm_mode = True


class EmployeeListResponse(BaseModel):
    """Schema for employee list response."""
    employees: List[EmployeeResponse] = Field(..., description="List of employees")
    pagination: dict = Field(..., description="Pagination information")


class EmployeeSearchFilter(BaseModel):
    """Schema for employee search filters."""
    search: Optional[str] = Field(None, description="Search term for name or emp_id")
    role: Optional[str] = Field(None, description="Filter by role")
    department_name: Optional[str] = Field(None, description="Filter by department")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page")
