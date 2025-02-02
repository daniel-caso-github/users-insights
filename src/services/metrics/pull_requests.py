from collections import Counter
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService
from opt.constans.order_service import OderService


class RepositoriesWithMorePRs(BaseGitHubMetric):
    """
    A GitHub metric that identifies the repositories where a user has contributed
    the most Pull Requests (PRs), focusing on merged PRs.

    This metric queries GitHub's search API to count the number of PRs the user
    has authored across repositories efficiently.

    Attributes:
        order (int): Defines the execution order of the metric (default: 2).
        logger (Logger): Logger instance for logging metric execution details.

    Methods:
        execute(username): Retrieves the top repositories where the user has submitted the most merged PRs.
    """

    def __init__(self):
        super().__init__()
        self.order = OderService.repositories_with_more_prs.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()
        self.max_results_per_page = self.get_setting("MAX_RESULTS_PER_PAGE")
        self.max_pages = self.get_setting("MAX_PAGES")

    def execute(self, username):
        """
        Retrieves the repositories where the user has submitted the most merged Pull Requests.

        Args:
            username (str): The GitHub username to analyze.

        Returns:
            dict: A structured response containing the top repositories and the count of merged PRs.

        If no PRs are found, the response will contain an empty list.
        """

        self.logger.info(f"📊 Starting PR repository analysis for {username}")

        repos_counter = Counter()
        page = 1

        while page <= self.max_pages:
            path = f"/search/issues?q=author:{username}+type:pr+is:merged&per_page={self.max_results_per_page}&page={page}"
            response = self.github_client_service.request_with_rate_limit(path)

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
            self.logger.warning(f"⚠️ No Pull Requests found for {username}")
            return self.format_response("repos_with_more_prs", [])

        formatted_repos = [
            {"repository": repo, "count": count}
            for repo, count in repos_counter.most_common(3)
        ]

        self.logger.info(f"✅ Top PR repositories for {username}: {formatted_repos}")

        return self.format_response("repos_with_more_prs", formatted_repos)
