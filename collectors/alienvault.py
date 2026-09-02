"""
AlienVault OTX Collector
Collects IOCs from AlienVault Open Threat Exchange (OTX).
API docs: https://otx.alienvault.com/api
"""

from datetime import UTC, datetime

import httpx
from loguru import logger

from collectors.base import BaseCollector
from config.loader import settings
from database.models import IOC


class AlienVaultCollector(BaseCollector):
    """Collects IOCs from AlienVault OTX subscribed pulses."""

    name = "alienvault"
    BASE_URL = "https://otx.alienvault.com/api/v1"

    def collect(self) -> list[dict]:
        """Fetch indicators from subscribed OTX pulses."""
        if not settings.alienvault_api_key:
            logger.warning(f"[{self.name}] No API key configured — skipping")
            return []

        response = httpx.get(
            f"{self.BASE_URL}/pulses/subscribed",
            headers={"X-OTX-API-KEY": settings.alienvault_api_key},
            params={"limit": 10},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        indicators = []
        for pulse in data.get("results", []):
            for indicator in pulse.get("indicators", []):
                indicator["_pulse_name"] = pulse.get("name", "")
                indicator["_pulse_tags"] = pulse.get("tags", [])
                indicators.append(indicator)
        return indicators

    def normalize(self, raw_records: list[dict]) -> list[IOC]:
        """Convert OTX indicators into standard IOC objects."""
        type_map = {
            "IPv4": "ip",
            "IPv6": "ip",
            "domain": "domain",
            "hostname": "domain",
            "URL": "url",
            "FileHash-MD5": "md5",
            "FileHash-SHA1": "sha1",
            "FileHash-SHA256": "sha256",
            "email": "email",
        }

        iocs = []
        for record in raw_records:
            try:
                ioc_type = type_map.get(record.get("type", ""))
                if not ioc_type:
                    continue

                tags = ["alienvault"] + record.get("_pulse_tags", [])

                ioc = IOC(
                    value=record["indicator"],
                    ioc_type=ioc_type,
                    source=self.name,
                    all_sources=[self.name],
                    threat_category="malware",
                    tags=tags,
                    confidence_score=70.0,
                    feed_reported_at=datetime.now(UTC),
                    raw=record,
                )
                iocs.append(ioc)
            except Exception as e:  # noqa: BLE001
                logger.warning(f"[{self.name}] Failed to normalize record: {e}")
                continue
        return iocs