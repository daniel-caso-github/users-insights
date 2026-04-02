import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level: str = "INFO") -> None:
    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    console = logging.StreamHandler()
    console.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        f"{LOG_DIR}/app.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root.addHandler(console)
    root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
