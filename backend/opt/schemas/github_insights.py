from typing import List, Optional

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


class UserProfile(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: Optional[str] = None
    followers: int = 0
    following: int = 0
    public_repos: int = 0


class SummaryStats(BaseModel):
    total_repos: int
    total_prs_merged: int
    merge_rate: int


class RecentEventItem(BaseModel):
    timestamp: str
    description: str
    event_type: str


class GitHubUserInsightsResponse(BaseModel):
    user_profile: Optional[UserProfile] = None
    most_used_languages: List[LanguageUsage] = []
    repos_with_more_prs: List[RepoPRs] = []
    monthly_contributions: List[MonthlyContributionItem] = []
    hours_more_activity: List[HourlyActivityItem] = []
    summary_stats: Optional[SummaryStats] = None
    recent_events: List[RecentEventItem] = []
