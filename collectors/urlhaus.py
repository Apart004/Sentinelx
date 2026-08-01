"""
URLHaus Collector
Collects malicious URLs from the URLHaus threat feed by abuse.ch.
API docs: https://urlhaus-api.abuse.ch/
No API key required.
"""

from datetime import UTC, datetime

import httpx
from loguru import logger

from collectors.base import BaseCollector
from database.models import IOC


class URLHausCollector(BaseCollector):
    """Collects malicious URLs from URLHaus public feed."""

    name = "urlhaus"
    FEED_URL = "https://urlhaus-api.abuse.ch/v1/urls/recent/limit/500/"

    def collect(self) -> list[dict]:
        """Fetch recent malicious URLs from URLHaus API."""
        response = httpx.post(
            self.FEED_URL,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("query_status") != "is_available":
            logger.warning(f"[{self.name}] Feed unavailable: {data.get('query_status')}")
            return []

        return data.get("urls", [])

    def normalize(self, raw_records: list[dict]) -> list[IOC]:
        """Convert URLHaus records into standard IOC objects."""
        iocs = []
        for record in raw_records:
            try:
                url = record.get("url", "").strip()
                if not url:
                    continue

                tags = ["urlhaus"]
                if record.get("tags"):
                    tags.extend(record["tags"])

                ioc = IOC(
                    value=url,
                    ioc_type="url",
                    source=self.name,
                    source_url=record.get("urlhaus_reference"),
                    all_sources=[self.name],
                    threat_category="malware",
                    tags=tags,
                    confidence_score=90.0,
                    feed_reported_at=datetime.now(UTC),
                    raw=record,
                )
                iocs.append(ioc)
            except Exception as e:  # noqa: BLE001
                logger.warning(f"[{self.name}] Failed to normalize record: {e}")
                continue
        return iocs
