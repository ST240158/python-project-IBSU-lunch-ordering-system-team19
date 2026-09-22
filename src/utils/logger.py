"""Centralised logging configuration for the IBSU Lunch Ordering System.

Uses Python's built-in ``logging`` module with both file and console handlers.
"""

import logging
import os
from datetime import datetime


def setup_logger(
    name: str = "ibsu_lunch",
    log_dir: str = "logs",
    level: int = logging.DEBUG,
) -> logging.Logger:
    """Configure and return a logger with file and console handlers.

    Args:
        name: Logger name.
        log_dir: Directory where the log file is stored.
        level: Minimum logging level.

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # File handler — detailed format for debugging / auditing
    log_filename = datetime.now().strftime("app_%Y%m%d.log")
    file_handler = logging.FileHandler(
        os.path.join(log_dir, log_filename), mode="a", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    # Console handler — concise format for the user
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        "%(levelname)s: %(message)s"
    )
    console_handler.setFormatter(console_fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
