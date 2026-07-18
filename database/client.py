"""
SentinelX Database Client
MongoDB connection with connection pooling.
"""

from loguru import logger
from pymongo import MongoClient
from pymongo.database import Database

from config.loader import settings


def get_client() -> MongoClient:
    """Create and return a MongoDB client with connection pooling."""
    client = MongoClient(
        settings.mongodb_uri,
        maxPoolSize=10,
        serverSelectionTimeoutMS=5000,
    )
    return client


def get_database() -> Database:
    """Return the SentinelX database instance."""
    client = get_client()
    db = client[settings.db_name]
    logger.info(f"Connected to MongoDB | db={settings.db_name}")
    return db
