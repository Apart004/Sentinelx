"""
SentinelX Database Models
Pydantic models defining the data schema for all platform entities.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class IOCType(str, Enum):
    """Supported Indicator of Compromise types."""

    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    EMAIL = "email"


class ThreatCategory(str, Enum):
    """Threat categories an IOC can be tagged with."""

    MALWARE = "malware"
    PHISHING = "phishing"
    C2 = "c2"
    SCANNER = "scanner"
    SPAM = "spam"
    EXPLOIT = "exploit"
    UNKNOWN = "unknown"


class IOC(BaseModel):
    """
    Core IOC (Indicator of Compromise) model.
    Every collector normalizes its output into this schema before storage.
    """

    # --- Identity ---
    value: str = Field(..., description="The raw IOC value (IP, domain, hash, etc.)")
    ioc_type: str = Field(
        ..., description="Type of indicator (ip, domain, url, md5, sha1, sha256, email)"
    )

    # --- Source tracking ---
    source: str = Field(..., description="Feed that first reported this IOC")
    source_url: Optional[str] = Field(None, description="Direct link to the source report")
    all_sources: list[str] = Field(
        default_factory=list,
        description="All feeds that have reported this IOC",
    )

    # --- Temporal ---
    first_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When SentinelX first observed this IOC",
    )
    last_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Most recent time this IOC was seen in any feed",
    )
    feed_reported_at: Optional[datetime] = Field(
        None,
        description="Timestamp from the source feed (may differ from first_seen)",
    )

    # --- Threat context ---
    threat_category: str = Field(
        default="unknown",
        description="Primary threat category",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Freeform tags (e.g. 'ransomware', 'apt29', 'emotet')",
    )
    malware_family: Optional[str] = Field(
        None,
        description="Malware family name if known (e.g. 'Emotet', 'Cobalt Strike')",
    )

    # --- Confidence & scoring ---
    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Confidence score 0-100. Increases as more feeds report this IOC.",
    )
    times_seen: int = Field(
        default=1,
        description="How many times this IOC has appeared across all feed pulls",
    )

    # --- Enrichment placeholder ---
    enriched: bool = Field(
        default=False,
        description="Whether enrichment pipeline has processed this IOC",
    )
    enrichment_data: dict = Field(
        default_factory=dict,
        description="Enrichment results (GeoIP, VT score, WHOIS, etc.)",
    )

    # --- Raw data ---
    raw: dict = Field(
        default_factory=dict,
        description="Original unmodified data from the source feed",
    )
