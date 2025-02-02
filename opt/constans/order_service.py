from enum import Enum


class OderService(int, Enum):
    language_most_used = 1
    repositories_with_more_prs = 2
    activity_recent = 3
    most_active_hours = 4
    default = 100
