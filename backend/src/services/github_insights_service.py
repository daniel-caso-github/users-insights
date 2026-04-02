import asyncio
import importlib
import pkgutil
import time
from pathlib import Path

import httpx
from fastapi import HTTPException, Depends

from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService
from opt.core.service import CoreService


class GitHubInsightsService(CoreService):
    def __init__(
        self,
        github_client_service: GitHubAPIService = Depends(),
    ):
        super().__init__()
        self.logger = self.get_logger(self.__class__.__name__)
        self.load_metrics()

        self.metrics = sorted(
            [metric() for metric in BaseGitHubMetric.__subclasses__()],
            key=lambda m: m.order,
        )
        self.github_client_service = github_client_service

        self.logger.info(
            f"Registered metrics: {[m.__class__.__name__ for m in self.metrics]}"
        )

    def load_metrics(self):
        metrics_path = Path(__file__).parent / "metrics"
        package_name = f"{__name__.rsplit('.', 1)[0]}.metrics"

        for module_info in pkgutil.iter_modules([str(metrics_path)]):
            module_name = f"{package_name}.{module_info.name}"
            if module_name not in globals():
                importlib.import_module(module_name)
                self.logger.debug(f"Imported metric module: {module_name}")

    async def user_exists(self, username: str, client: httpx.AsyncClient) -> bool:
        path = f"/users/{username}"
        response = await self.github_client_service.request_with_rate_limit(path, client)

        if not response or (
            "message" in response and response["message"] == "Not Found"
        ):
            self.logger.warning(f"User {username} not found on GitHub.")
            return False
        return True

    async def execute(self, username: str):
        self.logger.info(f"Starting data collection for user: {username}")
        total_start_time = time.time()

        async with httpx.AsyncClient() as client:
            if not await self.user_exists(username, client):
                raise HTTPException(
                    status_code=404, detail=f"User {username} not found on GitHub."
                )

            results = await asyncio.gather(
                *[metric.execute(username, client) for metric in self.metrics],
                return_exceptions=True,
            )

        result = {}
        for i, data in enumerate(results):
            if isinstance(data, Exception):
                self.logger.error(
                    f"{self.metrics[i].__class__.__name__} failed: {data}"
                )
            else:
                result.update(data)

        total_execution_time = time.time() - total_start_time
        self.logger.info(f"Collected insights for {username} in {total_execution_time:.2f}s")
        return result
