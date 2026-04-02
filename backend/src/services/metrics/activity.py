import asyncio
import time
from datetime import datetime, timedelta

import httpx

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService
from src.services.github_graphql_service import GitHubGraphQLService


_COMMITS_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
    }
  }
}
"""


class ActivityRecent(BaseGitHubMetric):
    def __init__(self):
        super().__init__()
        self.order = OderService.activity_recent.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()
        self.graphql_service = GitHubGraphQLService()

    async def execute(self, username: str, client: httpx.AsyncClient, repos: list | None = None) -> dict:
        today = datetime.today()
        months = [(today - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(6)]
        contributions = {
            month: {"pull_requests": 0, "issues": 0, "commits": 0} for month in months
        }

        self.logger.info(f"Starting contribution analysis for {username}")

        t0 = time.time()
        _, counts = await asyncio.gather(
            self.get_pr_issue_count(username, contributions, client),
            asyncio.gather(*[
                self._get_commits_for_month(username, month, client)
                for month in contributions.keys()
            ]),
        )
        self.logger.info(f"[TIMING] ActivityRecent gather (pr_issues + commits): {time.time() - t0:.2f}s")

        for month, count in zip(contributions.keys(), counts):
            contributions[month]["commits"] = count

        self.logger.debug(f"Final contributions for {username}: {contributions}")

        contributions_list = [
            {"month": month, **data} for month, data in contributions.items()
        ]
        return self.format_response("monthly_contributions", contributions_list)

    async def get_pr_issue_count(self, username: str, contributions: dict, client: httpx.AsyncClient):
        async def fetch_month(month, kind):
            start_date = f"{month}-01"
            end_date = self.get_last_day_of_month(month)
            path = f"/search/issues?q=author:{username}+type:{kind}+created:{start_date}..{end_date}"
            data = await self.github_client_service.request_with_rate_limit(path, client)
            count = data.get("total_count", 0) if data else 0
            return month, kind, count

        tasks = [
            fetch_month(month, kind)
            for month in contributions
            for kind in ("pr", "issue")
        ]
        results = await asyncio.gather(*tasks)

        for month, kind, count in results:
            key = "pull_requests" if kind == "pr" else "issues"
            contributions[month][key] = count
            self.logger.debug(f"{month} - {key}: {count}")

    async def _get_commits_for_month(self, username: str, month: str, client: httpx.AsyncClient) -> int:
        start = f"{month}-01T00:00:00Z"
        end = self.get_last_day_of_month(month) + "T23:59:59Z"
        data = await self.graphql_service.query(
            _COMMITS_QUERY,
            {"login": username, "from": start, "to": end},
            client,
        )
        if not data:
            return 0
        return data["user"]["contributionsCollection"]["totalCommitContributions"]

    @staticmethod
    def get_last_day_of_month(month):
        year, month = map(int, month.split("-"))
        if month == 12:
            return f"{year}-12-31"
        next_month = datetime(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return last_day.strftime("%Y-%m-%d")
