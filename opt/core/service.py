import logging
from src.config.settings import (
    Settings,
)
from opt.constans.order_service import OderService


class CoreService:
    """Centralized service for handling settings and logging configuration."""

    def __init__(self):
        """Initializes CoreService, loading settings and configuring logging."""
        self.settings = Settings()  # Load settings from environment variables
        self._configure_logging()
        self.order = OderService

    def _configure_logging(self):
        """Configures logging settings globally."""
        log_level = self.settings.LOG_LEVEL or "INFO"

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[logging.StreamHandler()],  # Logs printed to console
        )

    @staticmethod
    def get_logger(name: str):
        """Returns a logger instance for a given module/service."""
        return logging.getLogger(name)

    @staticmethod
    def get_header(token: str):
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_setting(self, key: str, default=None):
        """Retrieves a setting value, with an optional default."""
        return getattr(self.settings, key, default)
