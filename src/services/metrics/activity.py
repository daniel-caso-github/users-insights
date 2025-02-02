from datetime import datetime, timedelta

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class ActivityRecent(BaseGitHubMetric):
    """
    A GitHub metric that tracks the user's contributions (pull requests, issues, and commits)
    over the last six months.

    This metric gathers contributions from GitHub by fetching:
    - Pull requests created by the user.
    - Issues created by the user.
    - Commits made by the user across their repositories.

    Attributes:
        order (int): Defines the execution order of the metric (default: 3).
        logger (Logger): Logger instance for logging metric execution details.

    Methods:
        execute(username): Retrieves and processes the user's contribution data.
    """

    def __init__(self):
        """
        Initializes the metric with a predefined execution order and logger.
        """
        super().__init__()
        self.order = OderService.activity_recent.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    def execute(self, username):
        """
        Retrieves and processes the user's contributions (pull requests, issues, commits)
        over the last six months.

        Args:
            username (str): The GitHub username for which the contributions are analyzed.

        Returns:
            dict: A structured response containing the user's contributions per month.

        If no contributions are found, the response will contain empty values for each month.
        """
        today = datetime.today()
        months = [(today - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(6)]
        contributions = {
            month: {"pull_requests": 0, "issues": 0, "commits": 0}
            for month in sorted(months)
        }

        self.logger.info(f"📊 Starting contribution analysis for {username}")
        self.logger.info(f"📆 Last 6 months analyzed: {months}")

        for month in months:
            pr_count = self.get_pr_count(username, month)
            issue_count = self.get_issue_count(username, month)

            contributions[month]["pull_requests"] = pr_count
            contributions[month]["issues"] = issue_count

            self.logger.info(f"📌 {month} - PRs: {pr_count}, Issues: {issue_count}")

        repos = self.get_repositories(username)
        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}")
            return self.format_response("monthly_contributions", [])

        for repo in repos:
            self.logger.info(f"🔍 Searching commits in repository: {repo}")

            for month in months:
                commit_count = self.get_commit_count(username, repo, month)
                contributions[month]["commits"] += commit_count

                if commit_count > 0:
                    self.logger.info(f"✅ {month} - Commits in {repo}: {commit_count}")

        self.logger.info(f"✅ Final contributions for {username}: {contributions}")

        # 🔹 Convert dictionary into a structured list of objects.
        contributions_list = [
            {"month": month, **data} for month, data in contributions.items()
        ]

        return self.format_response("monthly_contributions", contributions_list)

    def get_pr_count(self, username, month):
        """
        Fetches the number of pull requests created by the user within a specific month.

        Args:
            username (str): The GitHub username.
            month (str): The month in "YYYY-MM" format.

        Returns:
            int: Number of pull requests created.
        """
        start_date = f"{month}-01"
        end_date = self.get_last_day_of_month(month)
        path = f"/search/issues?q=author:{username}+type:pr+created:{start_date}..{end_date}"
        data = self.github_client_service.request_with_rate_limit(path=path)

        count = data.get("total_count", 0) if data else 0
        self.logger.info(f"📌 PRs fetched for {username} in {month}: {count}")
        return count

    def get_issue_count(self, username, month):
        """
        Fetches the number of issues created by the user within a specific month.

        Args:
            username (str): The GitHub username.
            month (str): The month in "YYYY-MM" format.

        Returns:
            int: Number of issues created.
        """
        start_date = f"{month}-01"
        end_date = self.get_last_day_of_month(month)
        path = f"/search/issues?q=author:{username}+type:issue+created:{start_date}..{end_date}"
        data = self.github_client_service.request_with_rate_limit(path=path)

        count = data.get("total_count", 0) if data else 0
        self.logger.info(f"📌 Issues fetched for {username} in {month}: {count}")
        return count

    def get_repositories(self, username):
        """
        Fetches the repositories that the user has contributed to in the last 6 months.

        Args:
            username (str): The GitHub username.

        Returns:
            list: A list of repository names where the user has made contributions.
        """
        path = f"/users/{username}/repos?per_page=100"
        repos = self.github_client_service.request_with_rate_limit(path)

        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}")
            return []

        six_months_ago = datetime.utcnow() - timedelta(days=180)

        recent_repos = [
            repo["name"]
            for repo in repos
            if "pushed_at" in repo
            and datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
            >= six_months_ago
        ]

        self.logger.info(
            f"🔍 {len(recent_repos)} active repositories in the last 6 months for {username}: {recent_repos}"
        )

        return recent_repos

    def get_commit_count(self, username, repo, month):
        """
        Fetches the number of commits made by the user in a specific repository and month.

        Args:
            username (str): The GitHub username.
            repo (str): The repository name.
            month (str): The month in "YYYY-MM" format.

        Returns:
            int: Number of commits made.
        """
        start_date = f"{month}-01T00:00:00Z"
        end_date = self.get_last_day_of_month(month) + "T23:59:59Z"
        path = f"/repos/{username}/{repo}/commits?author={username}&since={start_date}&until={end_date}"
        commits = self.github_client_service.request_with_rate_limit(path=path)

        count = len(commits) if commits else 0
        self.logger.info(
            f"📌 Commits fetched for {username} in {repo} in {month}: {count}"
        )
        return count

    @staticmethod
    def get_last_day_of_month(month):
        """
        Determines the last day of a given month.

        Args:
            month (str): The month in "YYYY-MM" format.

        Returns:
            str: The last day of the month in "YYYY-MM-DD" format.
        """
        year, month = map(int, month.split("-"))
        if month == 12:
            return f"{year}-12-31"
        next_month = datetime(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return last_day.strftime("%Y-%m-%d")
