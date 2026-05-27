"""Logging Utilities"""

import logging
from pathlib import Path
from typing import Optional
from core.config import Config


def setup_logger(
    name: str = "deepseek-cli",
    log_level: str | None = None,
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """Setup application logger with optional file output.

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional path to log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level or Config.LOG_LEVEL))

    # Clear existing handlers
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(console_formatter)
        logger.addHandler(file_handler)

    return logger


# Default logger instance
logger = setup_logger()


__all__ = ["setup_logger", "logger"]
