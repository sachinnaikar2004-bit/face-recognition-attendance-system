"""
Database dependency injection.
"""

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import AsyncGenerator

from app.database.connection import get_db


async def get_database_dependency() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Dependency to get database instance."""
    async for db in get_db():
        yield db
