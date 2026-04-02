import asyncio
from datetime import datetime, timedelta

import httpx

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class ActivityRecent(BaseGitHubMetric):
    def __init__(self):
        super().__init__()
        self.order = OderService.activity_recent.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()
        self.max_results_per_page = self.get_setting("MAX_RESULTS_PER_PAGE")
        self.max_pages = self.get_setting("MAX_PAGES")

    async def execute(self, username: str, client: httpx.AsyncClient, repos: list | None = None) -> dict:
        today = datetime.today()
        months = [(today - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(6)]
        contributions = {
            month: {"pull_requests": 0, "issues": 0, "commits": 0} for month in months
        }

        self.logger.info(f"Starting contribution analysis for {username}")

        await self.get_pr_issue_count(username, contributions, client)

        if repos is None:
            repos = await self.get_repositories(username, client)
        else:
            six_months_ago = datetime.now() - timedelta(days=180)
            filtered = []
            for repo in repos:
                pushed_at = repo.get("pushed_at")
                if not pushed_at:
                    continue
                try:
                    if datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ") >= six_months_ago:
                        filtered.append(repo["name"])
                except ValueError:
                    pass
            repos = filtered
            self.logger.info(f"{len(repos)} active repos in last 6 months (pre-fetched)")

        if not repos:
            self.logger.warning(f"No repositories found for {username}")
            return self.format_response(
                "monthly_contributions",
                [{"month": month, **data} for month, data in contributions.items()],
            )

        await asyncio.gather(
            *[self.get_commit_count(username, repo, contributions, client) for repo in repos]
        )

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

    async def get_repositories(self, username: str, client: httpx.AsyncClient):
        path = f"/users/{username}/repos?per_page={self.max_results_per_page}"
        repos = await self.github_client_service.request_with_rate_limit(path, client)

        if not repos:
            self.logger.warning(f"No repositories found for {username}")
            return []

        six_months_ago = datetime.now() - timedelta(days=180)
        recent_repos = []

        for repo in repos:
            pushed_at = repo.get("pushed_at")
            if not pushed_at:
                self.logger.warning(
                    f"Repository {repo['name']} has no 'pushed_at' timestamp. Skipping."
                )
                continue

            try:
                last_pushed = datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ")
                if last_pushed >= six_months_ago:
                    recent_repos.append(repo["name"])
            except ValueError as e:
                self.logger.error(f"Error parsing pushed_at for {repo['name']}: {e}")

        self.logger.info(f"{len(recent_repos)} active repos in last 6 months")
        return recent_repos

    async def get_commit_count(self, username: str, repo: str, contributions: dict, client: httpx.AsyncClient):
        for month in contributions.keys():
            start_date = f"{month}-01T00:00:00Z"
            end_date = self.get_last_day_of_month(month) + "T23:59:59Z"
            page = 1
            commit_count = 0

            while page <= self.max_pages:
                path = f"/repos/{username}/{repo}/commits?author={username}&since={start_date}&until={end_date}&per_page={self.max_results_per_page}&page={page}"
                commits = await self.github_client_service.request_with_rate_limit(path, client)

                if not commits:
                    break

                commit_count += len(commits)

                if len(commits) < self.max_results_per_page:
                    break

                page += 1

            contributions[month]["commits"] += commit_count
            self.logger.debug(f"{month} - Commits in {repo}: {commit_count}")

    @staticmethod
    def get_last_day_of_month(month):
        year, month = map(int, month.split("-"))
        if month == 12:
            return f"{year}-12-31"
        next_month = datetime(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return last_day.strftime("%Y-%m-%d")
