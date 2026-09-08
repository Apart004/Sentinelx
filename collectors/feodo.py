"""
Feodo Tracker Collector
Collects C2 server IPs from Feodo Tracker by abuse.ch.
API docs: https://feodotracker.abuse.ch/api/
No API key required.
"""

from datetime import UTC, datetime

import httpx
from loguru import logger

from collectors.base import BaseCollector
from database.models import IOC


class FeodoCollector(BaseCollector):
    """Collects C2 IPs from Feodo Tracker public feed."""

    name = "feodo"
    FEED_URL = "https://feodotracker.abuse.ch/downloads/ipblocklist.json"

    def collect(self) -> list[dict]:
        """Fetch C2 IP blocklist from Feodo Tracker."""
        response = httpx.get(
            self.FEED_URL,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def normalize(self, raw_records: list[dict]) -> list[IOC]:
        """Convert Feodo records into standard IOC objects."""
        iocs = []
        for record in raw_records:
            try:
                ip = record.get("ip_address", "").strip()
                if not ip:
                    continue

                malware = record.get("malware", "")
                tags = ["feodo", "c2", "blocklist"]
                if malware:
                    tags.append(malware.lower())

                ioc = IOC(
                    value=ip,
                    ioc_type="ip",
                    source=self.name,
                    source_url="https://feodotracker.abuse.ch/browse/",
                    all_sources=[self.name],
                    threat_category="c2",
                    tags=tags,
                    malware_family=malware or None,
                    confidence_score=95.0,
                    feed_reported_at=datetime.now(UTC),
                    raw=record,
                )
                iocs.append(ioc)
            except Exception as e:  # noqa: BLE001
                logger.warning(f"[{self.name}] Failed to normalize record: {e}")
                continue
        return iocs
