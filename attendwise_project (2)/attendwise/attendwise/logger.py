"""Logging setup: events and errors are written to data/attendwise.log."""
import logging
import os

LOG_PATH = os.path.join("data", "attendwise.log")


def get_logger(name="attendwise", path=LOG_PATH):
    """Return a configured logger (created only once)."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        handler = logging.FileHandler(path, encoding="utf-8")
    except OSError:
        handler = logging.NullHandler()  # logging problems must never crash the app
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger
