import os
import time
import requests
from dotenv import load_dotenv

from config.logger_config import logger

# Load environment variables
load_dotenv()
GITHUB_API_URL = os.getenv("GITHUB_API_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Define request headers for GitHub API
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def request_with_rate_limit(path: str, retries=5):
    """
    Sends a GET request to the GitHub API while handling rate limits and retries.

    This function attempts to fetch data from GitHub while respecting the API's rate limits.
    If a request fails due to exceeding rate limits (HTTP 403 with rate limit headers),
    it waits until the reset time before retrying.

    Args:
        path (str): The API endpoint path (relative to GITHUB_API_URL).
        retries (int, optional): Number of retry attempts in case of failure. Defaults to 5.

    Returns:
        dict | list | None: JSON response data if the request succeeds, or None if it fails.

    Raises:
        Exception: If the request fails after all retry attempts.
    """
    parse_url = f"{GITHUB_API_URL}{path}"

    for attempt in range(retries):
        response = requests.get(parse_url, headers=HEADERS)

        if response.status_code == 200:
            return response.json()  # ✅ Successfully retrieved data

        elif (
            response.status_code == 403 and "X-RateLimit-Remaining" in response.headers
        ):
            # 🕒 Handle rate limits: wait for the reset time before retrying
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))
            wait_time = max(reset_time - int(time.time()), 1)
            logger.warning(
                f"⚠️ Rate limit reached. Waiting {wait_time} seconds before retrying..."
            )
            time.sleep(wait_time)

        else:
            # ❌ Log errors other than rate limit issues
            logger.error(f"❌ Error {response.status_code}: {response.text}")
            return None

    raise Exception("❌ Unable to complete the request after multiple attempts.")
