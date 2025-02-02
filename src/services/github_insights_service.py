import importlib
import pkgutil
from pathlib import Path
from fastapi import HTTPException, Depends
from src.services.base_metric import BaseGitHubMetric
from src.config.logger_config import get_logger
from src.services.github_client_service import GitHubAPIService


class GitHubInsightsService:
    """
    GitHubInsightsService is responsible for orchestrating and executing all registered GitHub metrics.

    This service dynamically loads metrics, validates if a GitHub user exists, and executes various
    analytics to provide insights into the user's activity, preferred languages, repository contributions,
    and more.

    Features:
    - Dynamically loads and sorts available GitHub metrics.
    - Validates if the specified GitHub user exists before running any metric.
    - Executes multiple metrics in an ordered manner.
    - Logs all relevant events for debugging and monitoring.
    - Handles API errors gracefully to prevent unnecessary requests.
    """

    def __init__(
            self,
            github_client_service: GitHubAPIService = Depends(),
    ):
        """
        Initializes the GitHubInsightsService.

        - Loads and registers all available metrics dynamically.
        - Sorts metrics based on their execution order.
        - Sets up a logger for tracking service execution.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.load_metrics()

        self.metrics = sorted(
            [metric() for metric in BaseGitHubMetric.__subclasses__()],
            key=lambda m: m.order,
        )
        self.github_client_service = github_client_service

        self.logger.info(
            f"🚀 Registered metrics (ordered): {[f'{m.__class__.__name__} (order={m.order})' for m in self.metrics]}"
        )

    def load_metrics(self):
        """
        Dynamically loads all metric modules from the 'metrics' directory.

        This allows new metrics to be added without modifying this class.
        """
        metrics_path = Path(__file__).parent / "metrics"
        package_name = f"{__name__.rsplit('.', 1)[0]}.metrics"

        for module_info in pkgutil.iter_modules([str(metrics_path)]):
            module_name = f"{package_name}.{module_info.name}"
            if module_name not in globals():
                importlib.import_module(module_name)
                self.logger.info(f"📥 Imported metric module: {module_name}")

    def user_exists(self, username: str) -> bool:
        """
        Checks if a GitHub user exists.

        Args:
            username (str): GitHub username to verify.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        path = f"/users/{username}"
        response = self.github_client_service.request_with_rate_limit(path=path)

        if not response or (
            "message" in response and response["message"] == "Not Found"
        ):
            self.logger.warning(f"⚠️ User {username} not found on GitHub.")
            return False
        return True

    def execute(self, username: str):
        """
        Collects and returns analytics data for a given GitHub user.

        - Validates if the user exists before executing metrics.
        - Runs all registered metrics in order.
        - Logs execution steps and errors if any occur.

        Args:
            username (str): The GitHub username for which insights are gathered.

        Returns:
            dict: A dictionary containing insights from all executed metrics.

        Raises:
            HTTPException: If the GitHub user does not exist.
        """
        self.logger.info(f"📡 Starting data collection for user: {username}")

        if not self.user_exists(username):
            raise HTTPException(
                status_code=404, detail=f"User {username} not found on GitHub."
            )

        result = {}

        for metric in self.metrics:
            try:
                self.logger.info(
                    f"🔍 Executing metric: {metric.__class__.__name__} (order={metric.order}) for {username}"
                )
                data = metric.execute(username)

                if not data:
                    self.logger.warning(
                        f"⚠️ Metric {metric.__class__.__name__} returned no data."
                    )

                self.logger.info(f"✅ Result of {metric.__class__.__name__}: {data}")

                result.update(data)
            except Exception as e:
                self.logger.error(
                    f"❌ Error executing {metric.__class__.__name__} for {username}: {e}"
                )

        self.logger.info(f"📊 Data collected for {username}: {result}")
        return result
