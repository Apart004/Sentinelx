"""
AbuseIPDB Collector
Collects malicious IP addresses from the AbuseIPDB threat feed.
API docs: https://docs.abuseipdb.com/#blacklist-endpoint
"""

from datetime import UTC, datetime

import httpx
from loguru import logger

from collectors.base import BaseCollector
from config.loader import settings
from database.models import IOC


class AbuseIPDBCollector(BaseCollector):
    """Collects malicious IPs from AbuseIPDB blacklist API."""

    name = "abuseipdb"

    def collect(self) -> list[dict]:
        """Fetch the AbuseIPDB blacklist (IPs with confidence >= 90)."""
        if not settings.abuseipdb_api_key:
            logger.warning(f"[{self.name}] No API key configured — skipping")
            return []

        response = httpx.get(
            "https://api.abuseipdb.com/api/v2/blacklist",
            headers={
                "Key": settings.abuseipdb_api_key,
                "Accept": "application/json",
            },
            params={
                "confidenceMinimum": 90,
                "limit": 1000,
            },
            timeout=settings.collector_timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    def normalize(self, raw_records: list[dict]) -> list[IOC]:
        """Convert AbuseIPDB records into standard IOC objects."""
        iocs = []
        for record in raw_records:
            try:
                ioc = IOC(
                    value=record["ipAddress"],
                    ioc_type="ip",
                    source=self.name,
                    source_url=f"https://www.abuseipdb.com/check/{record['ipAddress']}",
                    all_sources=[self.name],
                    threat_category="scanner",
                    tags=["abuseipdb", "blacklist"],
                    confidence_score=float(record.get("abuseConfidenceScore", 0)),
                    feed_reported_at=datetime.now(UTC),
                    raw=record,
                )
                iocs.append(ioc)
            except Exception as e:  # noqa: BLE001
                logger.warning(f"[{self.name}] Failed to normalize record: {e}")
                continue
        return iocs
