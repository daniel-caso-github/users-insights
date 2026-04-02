import logging
from src.config.settings import (
    Settings,
)
from opt.constans.order_service import OderService
from src.config.logger_config import setup_logging, get_logger


class CoreService:
    """Centralized service for handling settings and logging configuration."""

    def __init__(self):
        self.settings = Settings()
        setup_logging(self.settings.LOG_LEVEL or "INFO")
        self.order = OderService

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return get_logger(name)

    @staticmethod
    def get_header(token: str):
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_setting(self, key: str, default=None):
        """Retrieves a setting value, with an optional default."""
        return getattr(self.settings, key, default)
