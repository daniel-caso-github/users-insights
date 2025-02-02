import os
import time
import requests
from dotenv import load_dotenv

from opt.core.service import CoreService


class GitHubAPIService(CoreService):
    """A base service for making requests to the GitHub API, handling rate limits, and retries."""

    def __init__(self):
        super().__init__()
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_api_url = self.get_setting("GITHUB_API_URL")
        self.github_token = self.get_setting("GITHUB_TOKEN")
        self.headers = self.get_header(self.github_token)

    def request_with_rate_limit(self, path: str, retries=5):
        """
        Sends a GET request to the GitHub API while handling rate limits and retries.

        Args:
            path (str): The API endpoint path (relative to GITHUB_API_URL).
            retries (int, optional): Number of retry attempts in case of failure. Defaults to 5.

        Returns:
            dict | list | None: JSON response data if the request succeeds, or None if it fails.

        Raises:
            Exception: If the request fails after all retry attempts.
        """
        parse_url = f"{self.github_api_url}{path}"

        for attempt in range(retries):
            response = requests.get(parse_url, headers=self.headers)

            if response.status_code == 200:
                return response.json()  # ✅ Successfully retrieved data

            elif (
                response.status_code == 403 and "X-RateLimit-Remaining" in response.headers
            ):
                # 🕒 Handle rate limits: wait for the reset time before retrying
                reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))
                wait_time = max(reset_time - int(time.time()), 1)
                self.logger.warning(
                    f"⚠️ Rate limit reached. Waiting {wait_time} seconds before retrying..."
                )
                time.sleep(wait_time)

            else:
                # ❌ Log errors other than rate limit issues
                self.logger.error(f"❌ Error {response.status_code}: {response.text}")
                return None

        raise Exception("❌ Unable to complete the request after multiple attempts.")