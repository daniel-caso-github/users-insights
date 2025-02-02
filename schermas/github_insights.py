from typing import List

from pydantic import BaseModel


class LanguageUsage(BaseModel):
    language: str
    count: int


class RepoPRs(BaseModel):
    repository: str
    count: int


class MonthlyContributionItem(BaseModel):
    month: str
    pull_requests: int
    issues: int
    commits: int


class HourlyActivityItem(BaseModel):
    period: str
    count: int


class GitHubUserInsightsResponse(BaseModel):
    most_used_languages: List[LanguageUsage] = []
    repos_with_more_prs: List[RepoPRs] = []
    monthly_contributions: List[MonthlyContributionItem] = []
    hours_more_activity: List[HourlyActivityItem] = []
