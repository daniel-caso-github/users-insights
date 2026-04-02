from collections import Counter

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

    async def execute(self, username: str, client: httpx.AsyncClient) -> dict:
        self.logger.info(f"Starting PR repository analysis for {username}")

        repos_counter = Counter()
        page = 1

        while page <= self.max_pages:
            path = f"/search/issues?q=author:{username}+type:pr+is:merged&per_page={self.max_results_per_page}&page={page}"
            response = await self.github_client_service.request_with_rate_limit(path, client)

            if not response or "items" not in response:
                break

            for pr in response["items"]:
                repo_url = pr.get("repository_url")
                if repo_url:
                    repos_counter[repo_url] += 1

            if len(response["items"]) < self.max_results_per_page:
                break

            page += 1

        if not repos_counter:
            self.logger.warning(f"No Pull Requests found for {username}")
            return self.format_response("repos_with_more_prs", [])

        formatted_repos = [
            {"repository": repo, "count": count}
            for repo, count in repos_counter.most_common(3)
        ]

        self.logger.info(f"Top PR repositories for {username}: {formatted_repos}")

        return self.format_response("repos_with_more_prs", formatted_repos)
