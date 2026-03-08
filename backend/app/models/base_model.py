"""
Base model with common fields and methods.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId class for Pydantic serialization."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseDocument(BaseModel):
    """Base document model with common fields."""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
    def dict(self, **kwargs):
        """Convert to dictionary with proper ObjectId handling."""
        data = super().dict(**kwargs)
        if "_id" in data and data["_id"] is not None:
            data["_id"] = str(data["_id"])
        return data
    
    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> "BaseDocument":
        """Create instance from MongoDB document."""
        if not data:
            return None
        
        # Convert ObjectId to string for Pydantic
        if "_id" in data:
            data["_id"] = str(data["_id"])
        
        return cls(**data)
    
    def to_mongo(self) -> Dict[str, Any]:
        """Convert to MongoDB document format."""
        data = self.dict(by_alias=True)
        
        # Convert string back to ObjectId if needed
        if "_id" in data and isinstance(data["_id"], str):
            data["_id"] = ObjectId(data["_id"])
        
        return data
