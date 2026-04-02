import asyncio
from collections import Counter
from math import ceil

import httpx

from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService
from opt.constans.order_service import OderService


class RepositoriesWithMorePRs(BaseGitHubMetric):
    def __init__(self):
        super().__init__()
        self.order = OderService.repositories_with_more_prs.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()
        self.max_results_per_page = self.get_setting("MAX_RESULTS_PER_PAGE")
        self.max_pages = self.get_setting("MAX_PAGES")

    async def execute(self, username: str, client: httpx.AsyncClient, repos: list | None = None) -> dict:
        self.logger.info(f"Starting PR repository analysis for {username}")

        base_path = f"/search/issues?q=author:{username}+type:pr+is:merged&per_page={self.max_results_per_page}"

        first = await self.github_client_service.request_with_rate_limit(base_path + "&page=1", client)

        if not first or "items" not in first:
            self.logger.warning(f"No Pull Requests found for {username}")
            return self.format_response("repos_with_more_prs", [])

        total_count = first.get("total_count", 0)
        remaining_pages = min(ceil(total_count / self.max_results_per_page), self.max_pages) - 1

        all_items = list(first["items"])

        if remaining_pages > 0:
            rest = await asyncio.gather(*[
                self.github_client_service.request_with_rate_limit(base_path + f"&page={p}", client)
                for p in range(2, remaining_pages + 2)
            ])
            for r in rest:
                if r and "items" in r:
                    all_items.extend(r["items"])

        repos_counter = Counter()
        for pr in all_items:
            repo_url = pr.get("repository_url")
            if repo_url:
                repos_counter[repo_url] += 1

        if not repos_counter:
            self.logger.warning(f"No Pull Requests found for {username}")
            return self.format_response("repos_with_more_prs", [])

        formatted_repos = [
            {"repository": repo, "count": count}
            for repo, count in repos_counter.most_common(3)
        ]

        self.logger.info(f"Top PR repositories for {username}: {formatted_repos}")

        return self.format_response("repos_with_more_prs", formatted_repos)
