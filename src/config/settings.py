import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


class Settings:
    """Class to manage environment variables and application settings."""

    GITHUB_API_URL: str = os.getenv("GITHUB_API_URL", "https://api.github.com")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
