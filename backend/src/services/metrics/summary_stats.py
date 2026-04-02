import asyncio

import httpx

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class SummaryStatsMetric(BaseGitHubMetric):
    def __init__(self):
        super().__init__()
        self.order = OderService.summary_stats.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    async def execute(self, username: str, client: httpx.AsyncClient, repos: list | None = None) -> dict:
        profile_path = f"/users/{username}"
        prs_path = f"/search/issues?q=author:{username}+type:pr"
        merged_path = f"/search/issues?q=author:{username}+type:pr+is:merged"

        profile_data, prs_data, merged_data = await asyncio.gather(
            self.github_client_service.request_with_rate_limit(profile_path, client),
            self.github_client_service.request_with_rate_limit(prs_path, client),
            self.github_client_service.request_with_rate_limit(merged_path, client),
        )

        total_repos = profile_data.get("public_repos", 0) if profile_data else 0
        total_prs = prs_data.get("total_count", 0) if prs_data else 0
        total_merged = merged_data.get("total_count", 0) if merged_data else 0
        merge_rate = round(total_merged / total_prs * 100) if total_prs > 0 else 0

        stats = {
            "total_repos": total_repos,
            "total_prs_merged": total_merged,
            "merge_rate": merge_rate,
        }
        return self.format_response("summary_stats", stats)
