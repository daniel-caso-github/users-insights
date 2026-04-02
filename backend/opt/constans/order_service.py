from enum import Enum


class OderService(int, Enum):
    user_profile = 0
    language_most_used = 1
    repositories_with_more_prs = 2
    activity_recent = 3
    most_active_hours = 4
    summary_stats = 5
    recent_events = 6
    default = 100
