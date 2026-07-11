"""
SentinelX Logging Configuration
Sets up loguru with console + file output, log rotation, and consistent formatting.
"""

import sys

from loguru import logger

from config.loader import settings


def setup_logging() -> None:
    """
    Configure loguru for SentinelX.
    Call this once at application startup — all modules then just import logger from loguru.
    """

    # Remove loguru's default handler (plain stderr with no formatting control)
    logger.remove()

    # Console handler — human-readable, colorized, for development
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # File handler — rotation, retention, for production debugging
    logger.add(
        settings.log_file,
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}",
        rotation=settings.log_rotation,
        retention=settings.log_retention,
        encoding="utf-8",
    )

    logger.info(f"Logging initialized | level={settings.log_level} | file={settings.log_file}")
