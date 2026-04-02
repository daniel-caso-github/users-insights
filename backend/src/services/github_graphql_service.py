import httpx

from opt.core.service import CoreService


class GitHubGraphQLService(CoreService):
    GRAPHQL_URL = "https://api.github.com/graphql"

    def __init__(self):
        super().__init__()
        self.logger = self.get_logger(self.__class__.__name__)

    async def query(self, query: str, variables: dict, client: httpx.AsyncClient) -> dict | None:
        payload = {"query": query, "variables": variables}
        response = await client.post(
            self.GRAPHQL_URL,
            json=payload,
            headers=self.get_header(self.settings.GITHUB_TOKEN),
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("data")
        self.logger.error(f"GraphQL error {response.status_code}: {response.text[:200]}")
        return None
