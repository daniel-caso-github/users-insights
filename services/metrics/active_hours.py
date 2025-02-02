from config.logger_config import get_logger
from services.base_metric import BaseGitHubMetric
from services.github_client import request_with_rate_limit


class MostActiveHours(BaseGitHubMetric):
    """
    A GitHub metric that calculates the user's most active hours based on public events.

    This metric retrieves the latest public events of a GitHub user and categorizes
    their activity into three periods: morning, afternoon, and evening.

    Attributes:
        order (int): Defines the execution order of the metric (default: 4).
        logger (Logger): Logger instance for logging metric execution details.

    Methods:
        get_data(username): Retrieves and processes the user's activity data.
    """

    def __init__(self):
        """
        Initializes the metric with a predefined execution order and logger.
        """
        super().__init__()
        self.order = 4
        self.logger = get_logger(self.__class__.__name__)

    def get_data(self, username):
        """
        Retrieves the user's activity from GitHub public events and categorizes it into time periods.

        Args:
            username (str): The GitHub username for which the activity is analyzed.

        Returns:
            dict: A structured response containing the user's activity count per time period.

        The time periods are:
            - "morning" (00:00 - 11:59)
            - "afternoon" (12:00 - 17:59)
            - "evening" (18:00 - 23:59)

        If no events are found, the response defaults to zero counts for all periods.
        """
        self.logger.info(f"📊 Starting hourly activity analysis for {username}")

        path = f"/users/{username}/events/public"
        events = request_with_rate_limit(path=path)

        # 🔹 Ensure the base structure always includes 0 values.
        activity_per_hour = {"morning": 0, "afternoon": 0, "evening": 0}

        if not events:
            self.logger.warning(
                f"⚠️ No events found for {username}. Returning default values (0)."
            )
        else:
            for event in events:
                hour = int(event["created_at"][11:13])
                if hour < 12:
                    activity_per_hour["morning"] += 1
                elif 12 <= hour < 18:
                    activity_per_hour["afternoon"] += 1
                else:
                    activity_per_hour["evening"] += 1

            self.logger.info(
                f"✅ Hourly activity analyzed for {username}: {activity_per_hour}"
            )

        # 🔹 Convert dictionary into a structured list of objects.
        hours_activity_list = [
            {"period": period, "count": count}
            for period, count in activity_per_hour.items()
        ]

        return self.format_response("hours_more_activity", hours_activity_list)
