from datetime import datetime

from opt.constans.order_service import OderService
from src.services.base_metric import BaseGitHubMetric
from src.services.github_client_service import GitHubAPIService


class MostActiveHours(BaseGitHubMetric):
    """
    A GitHub metric that calculates the user's most active hours based on multiple sources:
    - Public events
    - Issues and PRs created by the user
    - Commits in repositories

    This provides a more **accurate** representation of the user's activity.
    """

    def __init__(self):
        """Initializes the metric with a predefined execution order and logger."""
        super().__init__()
        self.order = OderService.most_active_hours.value
        self.logger = self.get_logger(self.__class__.__name__)
        self.github_client_service = GitHubAPIService()

    def execute(self, username):
        """
        Retrieves the user's activity timestamps from multiple sources and categorizes them into:
            - "morning" (00:00 - 11:59)
            - "afternoon" (12:00 - 17:59)
            - "evening" (18:00 - 23:59)
        """
        self.logger.info(f"📊 Starting hourly activity analysis for {username}")

        events = self.get_public_events(username)

        issues_prs = self.get_issues_and_prs(username)

        commits = self.get_recent_commits(username)

        all_events = events + issues_prs + commits
        activity_per_hour = self.categorize_by_hour(all_events)

        self.logger.info(
            f"✅ Hourly activity analyzed for {username}: {activity_per_hour}"
        )

        hours_activity_list = [
            {"period": period, "count": count}
            for period, count in activity_per_hour.items()
        ]

        return self.format_response("hours_more_activity", hours_activity_list)

    def get_public_events(self, username):
        """Fetches timestamps from public events."""
        path = f"/users/{username}/events/public"
        events = self.github_client_service.request_with_rate_limit(path=path)

        if not events:
            self.logger.warning(f"⚠️ No public events found for {username}.")
            return []

        return [event["created_at"] for event in events if "created_at" in event]

    def get_issues_and_prs(self, username):
        """Fetches timestamps from issues and pull requests created by the user."""
        path = f"/search/issues?q=author:{username}"
        data = self.github_client_service.request_with_rate_limit(path=path)

        if not data or "items" not in data:
            self.logger.warning(f"⚠️ No issues or PRs found for {username}.")
            return []

        return [item["created_at"] for item in data["items"] if "created_at" in item]

    def get_recent_commits(self, username):
        """Fetches timestamps from recent commits in the user's repositories."""
        path = (
            f"/users/{username}/repos?per_page=10"
        )
        repos = self.github_client_service.request_with_rate_limit(path)

        if not repos:
            self.logger.warning(f"⚠️ No repositories found for {username}.")
            return []

        commit_timestamps = []
        for repo in repos[:5]:
            repo_name = repo["name"]
            commits_path = (
                f"/repos/{username}/{repo_name}/commits?author={username}&per_page=5"
            )
            commits = self.github_client_service.request_with_rate_limit(commits_path)

            if not commits:
                continue

            commit_timestamps.extend(
                [
                    commit["commit"]["committer"]["date"]
                    for commit in commits
                    if "commit" in commit
                ]
            )

        return commit_timestamps

    def categorize_by_hour(self, timestamps):
        """
        Categorizes timestamps into morning, afternoon, and evening activity.

        Returns:
            dict: A dictionary with counts per period.
        """
        activity_per_hour = {"morning": 0, "afternoon": 0, "evening": 0}

        for timestamp in timestamps:
            try:
                hour = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").hour
                if hour < 12:
                    activity_per_hour["morning"] += 1
                elif 12 <= hour < 18:
                    activity_per_hour["afternoon"] += 1
                else:
                    activity_per_hour["evening"] += 1
            except Exception as e:
                self.logger.error(f"❌ Error parsing timestamp {timestamp}: {e}")

        return activity_per_hour
