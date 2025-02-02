from datetime import datetime, timedelta

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class ActivityRecent(BaseGitHubMetric):
    """
    A GitHub metric that tracks the user's contributions (pull requests, issues, and commits)
    over the last six months.

    This metric gathers contributions from GitHub by efficiently fetching:
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
        """Initializes the metric with a predefined execution order and logger."""
        super().__init__()
        self.order = OderService.activity_recent.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()
        self.max_results_per_page = self.get_setting("MAX_RESULTS_PER_PAGE")
        self.max_pages = self.get_setting("MAX_PAGES")

    def execute(self, username):
        """
        Retrieves and processes the user's contributions (pull requests, issues, commits)
        over the last six months.

        Args:
            username (str): The GitHub username.

        Returns:
            dict: A structured response containing the user's contributions per month.
        """
        today = datetime.today()
        months = [(today - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(6)]
        contributions = {
            month: {"pull_requests": 0, "issues": 0, "commits": 0} for month in months
        }

        self.logger.info(f"📊 Starting contribution analysis for {username}")
        self.logger.info(f"📆 Last 6 months analyzed: {months}")

        self.get_pr_issue_count(username, contributions)

        repos = self.get_repositories(username)
        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}")
            return self.format_response(
                "monthly_contributions",
                [{"month": month, **data} for month, data in contributions.items()],
            )

        for repo in repos:
            self.logger.info(f"🔍 Searching commits in repository: {repo}")
            self.get_commit_count(username, repo, contributions)

        self.logger.info(f"✅ Final contributions for {username}: {contributions}")

        contributions_list = [
            {"month": month, **data} for month, data in contributions.items()
        ]
        return self.format_response("monthly_contributions", contributions_list)

    def get_pr_issue_count(self, username, contributions):
        """
        Fetches the number of pull requests and issues created by the user in the last 6 months.
        """
        for month in contributions.keys():
            start_date = f"{month}-01"
            end_date = self.get_last_day_of_month(month)

            # 🔹 PRs
            pr_path = f"/search/issues?q=author:{username}+type:pr+created:{start_date}..{end_date}"
            pr_data = self.github_client_service.request_with_rate_limit(pr_path)
            contributions[month]["pull_requests"] = (
                pr_data.get("total_count", 0) if pr_data else 0
            )

            # 🔹 Issues
            issue_path = f"/search/issues?q=author:{username}+type:issue+created:{start_date}..{end_date}"
            issue_data = self.github_client_service.request_with_rate_limit(issue_path)
            contributions[month]["issues"] = (
                issue_data.get("total_count", 0) if issue_data else 0
            )

            self.logger.info(
                f"📌 {month} - PRs: {contributions[month]['pull_requests']}, Issues: {contributions[month]['issues']}"
            )

    def get_repositories(self, username):
        """
        Fetches the repositories that the user has contributed to in the last 6 months.
        """
        path = f"/users/{username}/repos?per_page={self.max_results_per_page}"
        repos = self.github_client_service.request_with_rate_limit(path)

        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}")
            return []

        six_months_ago = datetime.now() - timedelta(days=180)
        recent_repos = []

        for repo in repos:
            pushed_at = repo.get("pushed_at")
            if not pushed_at:
                self.logger.warning(
                    f"⚠️ Repository {repo['name']} has no 'pushed_at' timestamp. Skipping."
                )
                continue

            try:
                last_pushed = datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ")
                if last_pushed >= six_months_ago:
                    recent_repos.append(repo["name"])
            except ValueError as e:
                self.logger.error(f"❌ Error parsing pushed_at for {repo['name']}: {e}")

        self.logger.info(
            f"🔍 {len(recent_repos)} active repositories in last 6 months: {recent_repos}"
        )
        return recent_repos

    def get_commit_count(self, username, repo, contributions):
        """
        Fetches the number of commits made by the user in each month for a given repository.
        """
        for month in contributions.keys():
            start_date = f"{month}-01T00:00:00Z"
            end_date = self.get_last_day_of_month(month) + "T23:59:59Z"
            page = 1
            commit_count = 0

            while page <= self.max_pages:
                path = f"/repos/{username}/{repo}/commits?author={username}&since={start_date}&until={end_date}&per_page={self.max_results_per_page}&page={page}"
                commits = self.github_client_service.request_with_rate_limit(path)

                if not commits:
                    break

                commit_count += len(commits)

                if len(commits) < self.max_results_per_page:
                    break

                page += 1

            contributions[month]["commits"] += commit_count
            self.logger.info(f"✅ {month} - Commits in {repo}: {commit_count}")

    @staticmethod
    def get_last_day_of_month(month):
        """
        Determines the last day of a given month.
        """
        year, month = map(int, month.split("-"))
        if month == 12:
            return f"{year}-12-31"
        next_month = datetime(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return last_day.strftime("%Y-%m-%d")
