import asyncio
import time

import httpx

from opt.core.service import CoreService


class GitHubAPIService(CoreService):
    """A base service for making requests to the GitHub API, handling rate limits, and retries."""

    def __init__(self):
        super().__init__()
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_api_url = self.get_setting("GITHUB_API_URL")
        self.github_token = self.get_setting("GITHUB_TOKEN")
        self.headers = self.get_header(self.github_token)

    async def request_with_rate_limit(self, path: str, client: httpx.AsyncClient, retries=5) -> dict | list | None:
        url = f"{self.github_api_url}{path}"

        for attempt in range(retries):
            self.logger.debug(f"GET {path} (attempt {attempt + 1}/{retries})")
            response = await client.get(url, headers=self.headers)

            if response.status_code == 200:
                return response.json()

            elif (
                response.status_code == 403
                and "X-RateLimit-Remaining" in response.headers
            ):
                reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))
                wait_time = max(reset_time - int(time.time()), 1)
                self.logger.warning(
                    f"Rate limit hit on {path}. Waiting {wait_time}s..."
                )
                await asyncio.sleep(wait_time)

            else:
                self.logger.error(f"HTTP {response.status_code} on {path}")
                return None

        raise Exception(f"Failed after {retries} attempts: {path}")
