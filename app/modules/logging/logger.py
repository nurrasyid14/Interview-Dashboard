# app/modules/logging/logger.py
"""
Central logging utility for the AI Interview Evaluation System.

Features:
- Supports console + file logging
- Automatically creates log directories
- Can log general events or user-specific events
"""

import logging
from logging import Logger
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("app/data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "pipeline", level: int = logging.INFO) -> Logger:
    """
    Returns a configured logger instance.
    Logs will go to both console and rotating file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

        # File handler
        log_file = LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        fh.setLevel(level)
        fh_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    return logger


def log_user_event(user_id: str, message: str, level: int = logging.INFO):
    """
    Logs a user-specific event to a file named after the user ID.
    """
    user_log_dir = LOG_DIR / "users"
    user_log_dir.mkdir(exist_ok=True, parents=True)
    user_log_file = user_log_dir / f"{user_id}.log"

    user_logger = logging.getLogger(f"user_{user_id}")
    user_logger.setLevel(level)

    if not user_logger.hasHandlers():
        fh = logging.FileHandler(user_log_file, mode="a", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        user_logger.addHandler(fh)

    user_logger.log(level, message)
