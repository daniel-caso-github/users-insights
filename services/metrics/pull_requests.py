from collections import Counter
from config.logger_config import get_logger
from services.base_metric import BaseGitHubMetric
from services.github_client import request_with_rate_limit


class RepositoriesWithMorePRs(BaseGitHubMetric):
    """
    A GitHub metric that identifies the repositories where a user has contributed
    the most Pull Requests (PRs), focusing on merged PRs.

    This metric queries GitHub's search API to count the number of PRs the user
    has authored across repositories.

    Attributes:
        order (int): Defines the execution order of the metric (default: 2).
        logger (Logger): Logger instance for logging metric execution details.

    Methods:
        get_data(username): Retrieves the top repositories where the user has submitted the most merged PRs.
    """

    def __init__(self):
        """
        Initializes the metric with a predefined execution order and logger.
        """
        super().__init__()
        self.order = 2
        self.logger = get_logger(self.__class__.__name__)

    def get_data(self, username):
        """
        Retrieves the repositories where the user has submitted the most merged Pull Requests.

        Args:
            username (str): The GitHub username to analyze.

        Returns:
            dict: A structured response containing the top repositories and the count of merged PRs.

        If no PRs are found, the response will contain an empty list.
        """
        self.logger.info(f"📊 Starting PR repository analysis for {username}")

        path = f"/search/issues?q=author:{username}+type:pr+is:merged"
        prs = request_with_rate_limit(path)

        if not prs or "items" not in prs:
            self.logger.warning(f"⚠️ No Pull Requests found for {username}")
            return self.format_response(
                "repos_with_more_prs", []
            )  # Always return a list

        # Count the occurrences of PRs per repository
        repos = Counter(pr["repository_url"] for pr in prs["items"])
        formatted_repos = [
            {"repository": repo, "count": count} for repo, count in repos.most_common(3)
        ]

        self.logger.info(f"✅ Top PR repositories for {username}: {formatted_repos}")

        return self.format_response("repos_with_more_prs", formatted_repos)
