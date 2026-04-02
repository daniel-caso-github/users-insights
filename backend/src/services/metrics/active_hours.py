import asyncio
from datetime import datetime

import httpx

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class MostActiveHours(BaseGitHubMetric):
    def __init__(self):
        super().__init__()
        self.order = OderService.most_active_hours.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    async def execute(self, username: str, client: httpx.AsyncClient, repos: list | None = None) -> dict:
        self.logger.info(f"Starting hourly activity analysis for {username}")

        events, issues_prs, commits = await asyncio.gather(
            self.get_public_events(username, client),
            self.get_issues_and_prs(username, client),
            self.get_recent_commits(username, client, repos=repos),
        )

        all_events = events + issues_prs + commits
        activity_per_hour = self.categorize_by_hour(all_events)

        self.logger.debug(f"Hourly activity analyzed for {username}: {activity_per_hour}")
        self.logger.info(f"Hourly activity analyzed for {username}")

        hours_activity_list = [
            {"period": period, "count": count}
            for period, count in activity_per_hour.items()
        ]

        return self.format_response("hours_more_activity", hours_activity_list)

    async def get_public_events(self, username: str, client: httpx.AsyncClient):
        path = f"/users/{username}/events/public"
        events = await self.github_client_service.request_with_rate_limit(path, client)

        if not events:
            self.logger.warning(f"No public events found for {username}.")
            return []

        return [event["created_at"] for event in events if "created_at" in event]

    async def get_issues_and_prs(self, username: str, client: httpx.AsyncClient):
        path = f"/search/issues?q=author:{username}"
        data = await self.github_client_service.request_with_rate_limit(path, client)

        if not data or "items" not in data:
            self.logger.warning(f"No issues or PRs found for {username}.")
            return []

        return [item["created_at"] for item in data["items"] if "created_at" in item]

    async def get_recent_commits(self, username: str, client: httpx.AsyncClient, repos: list | None = None):
        if repos is None:
            path = f"/users/{username}/repos?per_page=10"
            repos = await self.github_client_service.request_with_rate_limit(path, client)

        if not repos:
            self.logger.warning(f"No repositories found for {username}.")
            return []

        async def fetch_repo_commits(repo):
            repo_name = repo["name"]
            commits_path = f"/repos/{username}/{repo_name}/commits?author={username}&per_page=5"
            commits = await self.github_client_service.request_with_rate_limit(commits_path, client)
            if not commits:
                return []
            return [
                commit["commit"]["committer"]["date"]
                for commit in commits
                if "commit" in commit
            ]

        results = await asyncio.gather(*[fetch_repo_commits(repo) for repo in repos[:5]])
        commit_timestamps = []
        for r in results:
            commit_timestamps.extend(r)
        return commit_timestamps

    def categorize_by_hour(self, timestamps):
        activity_per_hour = {"morning": 0, "afternoon": 0, "evening": 0}

        for timestamp in timestamps:
            try:
                hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").hour
                if hour < 12:
                    activity_per_hour["morning"] += 1
                elif 12 <= hour < 18:
                    activity_per_hour["afternoon"] += 1
                else:
                    activity_per_hour["evening"] += 1
            except Exception as e:
                self.logger.error(f"Error parsing timestamp {timestamp}: {e}")

        return activity_per_hour
