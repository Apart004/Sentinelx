"""
SentinelX Database Indexes
Define and create MongoDB indexes for optimal query performance.
"""

from loguru import logger
from pymongo.database import Database


def create_indexes(db: Database) -> None:
    """Create all required indexes for SentinelX collections."""

    # IOC collection indexes
    iocs = db["iocs"]

    # Primary lookup — find IOC by value (e.g. search for "1.2.3.4")
    iocs.create_index("value", unique=True)

    # Filter by type (e.g. show all malicious IPs)
    iocs.create_index("ioc_type")

    # Filter by source feed
    iocs.create_index("source")

    # Sort/filter by confidence score
    iocs.create_index("confidence_score")

    # Find recently seen IOCs
    iocs.create_index("last_seen")

    # Compound index — most common query pattern: type + confidence
    iocs.create_index([("ioc_type", 1), ("confidence_score", -1)])

    logger.info("MongoDB indexes created successfully")