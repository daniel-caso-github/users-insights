import httpx

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class UserProfileMetric(BaseGitHubMetric):
    def __init__(self):
        super().__init__()
        self.order = OderService.user_profile.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    async def execute(self, username: str, client: httpx.AsyncClient) -> dict:
        path = f"/users/{username}"
        data = await self.github_client_service.request_with_rate_limit(path, client)

        if not data:
            return self.format_response("user_profile", None)

        profile = {
            "name": data.get("name"),
            "bio": data.get("bio"),
            "company": data.get("company"),
            "location": data.get("location"),
            "avatar_url": data.get("avatar_url"),
            "html_url": data.get("html_url"),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "public_repos": data.get("public_repos", 0),
        }
        return self.format_response("user_profile", profile)
