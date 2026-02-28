"""Configure Python logging for the application."""
from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler


def setup_logging() -> None:
    """Set up root logger with stderr handler and optional rotating file handler.

    Reads LOG_LEVEL (default "INFO") and LOG_FILE (default "") from config.
    """
    from app.config import LOG_LEVEL, LOG_FILE

    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-5s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(level)

    # stderr handler (always attached)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(level)
    stderr_handler.setFormatter(fmt)
    root.addHandler(stderr_handler)

    # rotating file handler (only when LOG_FILE is set)
    if LOG_FILE:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(fmt)
        root.addHandler(file_handler)
