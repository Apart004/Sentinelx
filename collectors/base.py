"""
SentinelX Base Collector
Abstract base class that all feed collectors inherit from.
"""

from abc import ABC, abstractmethod
from datetime import UTC, datetime

import httpx
from loguru import logger

from config.loader import settings
from database.models import IOC


class BaseCollector(ABC):
    """
    Abstract base class for all threat intelligence feed collectors.

    Every collector must implement:
    - name: unique feed identifier
    - collect(): fetch raw data from the feed
    - normalize(): convert raw data into IOC objects
    """

    name: str = "base"

    def __init__(self):
        self.client = httpx.Client(
            timeout=settings.collector_timeout,
            headers={"User-Agent": f"SentinelX/{settings.app_version}"},
        )
        self.collected_at: datetime = datetime.now(UTC)
        self.stats = {
            "fetched": 0,
            "normalized": 0,
            "errors": 0,
        }

    @abstractmethod
    def collect(self) -> list[dict]:
        """
        Fetch raw data from the threat feed.
        Returns a list of raw records (dicts) from the source.
        """

    @abstractmethod
    def normalize(self, raw_records: list[dict]) -> list[IOC]:
        """
        Convert raw feed records into standardized IOC objects.
        Returns a list of IOC instances ready for storage.
        """

    def run(self) -> list[IOC]:
        """
        Main entry point — collect, normalize, log stats.
        Called by the scheduler for every feed on each run.
        """
        logger.info(f"[{self.name}] Starting collection")
        try:
            raw = self.collect()
            self.stats["fetched"] = len(raw)
            logger.info(f"[{self.name}] Fetched {len(raw)} raw records")

            iocs = self.normalize(raw)
            self.stats["normalized"] = len(iocs)
            logger.info(f"[{self.name}] Normalized {len(iocs)} IOCs")

            return iocs

        except httpx.TimeoutException:
            self.stats["errors"] += 1
            logger.error(f"[{self.name}] Request timed out")
            return []

        except httpx.HTTPError as e:
            self.stats["errors"] += 1
            logger.error(f"[{self.name}] HTTP error: {e}")
            return []

        except Exception as e:  # noqa: BLE001
            self.stats["errors"] += 1
            logger.error(f"[{self.name}] Unexpected error: {e}")
            return []

        finally:
            self.client.close()
            logger.info(f"[{self.name}] Stats: {self.stats}")
