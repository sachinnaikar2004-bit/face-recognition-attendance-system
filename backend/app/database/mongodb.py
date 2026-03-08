"""
MongoDB connection and database operations.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional
from app.core.config import settings
from app.core.exceptions import DatabaseException


class MongoDB:
    """MongoDB connection manager."""
    
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect_to_mongodb(cls) -> None:
        """Connect to MongoDB."""
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
            cls.database = cls.client.face_attendance
            
            # Test connection
            await cls.client.admin.command('ping')
            print("Successfully connected to MongoDB")
            
        except Exception as e:
            raise DatabaseException(f"Failed to connect to MongoDB: {str(e)}")
    
    @classmethod
    async def close_mongodb_connection(cls) -> None:
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed")
    
    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if not cls.database:
            raise DatabaseException("Database not connected")
        return cls.database
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get collection instance."""
        database = cls.get_database()
        return database[collection_name]


# Global database instance
db = MongoDB()


async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance for dependency injection."""
    return db.get_database()


async def init_db_indexes() -> None:
    """Initialize database indexes."""
    try:
        database = db.get_database()
        
        # Employees collection indexes
        await database.employees.create_index("emp_id", unique=True)
        await database.employees.create_index("email", unique=True)
        await database.employees.create_index("created_at")
        
        # Attendance collection indexes
        await database.attendance.create_index([("emp_id", 1), ("date", -1)])
        await database.attendance.create_index("date")
        await database.attendance.create_index("login_time")
        await database.attendance.create_index("created_at")
        
        print("Database indexes created successfully")
        
    except Exception as e:
        raise DatabaseException(f"Failed to create database indexes: {str(e)}")
