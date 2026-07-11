"""
SentinelX Configuration Loader
Merges config.yaml (non-secret settings) with .env (secrets) into a single settings object.
"""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from loguru import logger

# Load .env file first so environment variables are available
load_dotenv()

# Project root is two levels up from this file (config/loader.py -> root)
ROOT_DIR = Path(__file__).parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"


def _load_yaml(path: Path) -> dict:
    """Load and parse a YAML file."""
    if not path.exists():
        logger.warning(f"Config file not found at {path}, using defaults")
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


class Settings:
    """
    Central settings object for SentinelX.
    Combines config.yaml values with environment variables.
    Environment variables always take precedence over config.yaml.
    """

    def __init__(self):
        config = _load_yaml(CONFIG_PATH)

        # App
        app = config.get("app", {})
        self.app_name: str = app.get("name", "SentinelX")
        self.app_version: str = app.get("version", "0.1.0")
        self.env: str = app.get("env", "development")

        # Database — URI comes from .env, name from config.yaml
        self.mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db = config.get("database", {})
        self.db_name: str = db.get("name", "sentinelx")
        self.db_collections: dict = db.get("collections", {})

        # Logging
        log = config.get("logging", {})
        self.log_level: str = os.getenv("LOG_LEVEL", log.get("level", "INFO"))
        self.log_file: str = log.get("file", "logs/sentinelx.log")
        self.log_rotation: str = log.get("rotation", "10 MB")
        self.log_retention: str = log.get("retention", "30 days")

        # Collectors
        collectors = config.get("collectors", {})
        self.collector_interval: int = collectors.get("schedule_interval_minutes", 60)
        self.collector_timeout: int = collectors.get("timeout_seconds", 30)

        # Enrichment
        enrichment = config.get("enrichment", {})
        self.enrichment_cache_ttl: int = enrichment.get("cache_ttl_hours", 24)

        # API Keys — always from environment only, never hardcoded
        self.abuseipdb_api_key: str = os.getenv("ABUSEIPDB_API_KEY", "")
        self.alienvault_api_key: str = os.getenv("ALIENVAULT_API_KEY", "")
        self.virustotal_api_key: str = os.getenv("VIRUSTOTAL_API_KEY", "")
        self.shodan_api_key: str = os.getenv("SHODAN_API_KEY", "")


# Single instance — every module imports this object
settings = Settings()
