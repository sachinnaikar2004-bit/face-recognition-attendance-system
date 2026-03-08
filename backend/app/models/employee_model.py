"""
Employee data model.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import Field, validator
from app.models.base_model import BaseDocument


class Employee(BaseDocument):
    """Employee model."""
    
    emp_id: str = Field(..., description="Employee ID")
    name: str = Field(..., min_length=2, max_length=100, description="Employee name")
    email: str = Field(..., description="Employee email")
    role: str = Field(default="employee", description="Employee role")
    department: Optional[str] = Field(None, description="Department")
    face_encoding: List[float] = Field(default=[], description="Face encoding vector")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    is_active: bool = Field(default=True, description="Employee active status")
    
    @validator("email")
    def validate_email(cls, v):
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v
    
    @validator("role")
    def validate_role(cls, v):
        """Validate role."""
        allowed_roles = ["admin", "employee"]
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of: {allowed_roles}")
        return v
    
    @validator("face_encoding")
    def validate_face_encoding(cls, v):
        """Validate face encoding length."""
        if v and len(v) != 128:  # DeepFace VGG-Face produces 128-dimensional embeddings
            raise ValueError("Face encoding must be a 128-dimensional vector")
        return v
    
    class Config:
        collection_name = "employees"
        indexes = [
            {"keys": [("emp_id", 1)], "unique": True},
            {"keys": [("email", 1)], "unique": True},
            {"keys": [("created_at", -1)]},
        ]
    
    def has_face_encoding(self) -> bool:
        """Check if employee has face encoding."""
        return bool(self.face_encoding and len(self.face_encoding) == 128)
    
    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def activate(self):
        """Activate employee."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Deactivate employee."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
