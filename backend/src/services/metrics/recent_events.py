import httpx

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class RecentEventsMetric(BaseGitHubMetric):
    def __init__(self):
        super().__init__()
        self.order = OderService.recent_events.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    async def execute(self, username: str, client: httpx.AsyncClient) -> dict:
        path = f"/users/{username}/events/public?per_page=10"
        events = await self.github_client_service.request_with_rate_limit(path, client)

        if not events or not isinstance(events, list):
            return self.format_response("recent_events", [])

        result = [self._map_event(event) for event in events]
        return self.format_response("recent_events", result)

    def _map_event(self, event: dict) -> dict:
        event_type = event.get("type", "")
        repo = event.get("repo", {}).get("name", "unknown")
        payload = event.get("payload", {})

        return {
            "timestamp": event.get("created_at", ""),
            "description": self._describe_event(event_type, repo, payload),
            "event_type": event_type,
        }

    @staticmethod
    def _describe_event(event_type: str, repo: str, payload: dict) -> str:
        if event_type == "PushEvent":
            return f"Pushed commits to {repo}"
        elif event_type == "PullRequestEvent":
            return f"Pull request {payload.get('action', '')} in {repo}"
        elif event_type == "IssuesEvent":
            return f"Issue {payload.get('action', '')} in {repo}"
        elif event_type == "CreateEvent":
            return f"Created {payload.get('ref_type', '')} in {repo}"
        elif event_type == "WatchEvent":
            return f"Starred {repo}"
        elif event_type == "ForkEvent":
            return f"Forked {repo}"
        else:
            return f"{event_type} in {repo}"
