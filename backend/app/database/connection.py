"""
Database connection utilities and dependency injection.
"""

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import AsyncGenerator
from app.database.mongodb import db, get_database
from app.database.mongodb import init_db_indexes


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Get database dependency."""
    try:
        database = await get_database()
        yield database
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")


async def init_database() -> None:
    """Initialize database connection and indexes."""
    await db.connect_to_mongodb()
    await init_db_indexes()


async def close_database() -> None:
    """Close database connection."""
    await db.close_mongodb_connection()
