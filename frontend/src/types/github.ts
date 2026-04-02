export interface UserProfile {
  name: string | null
  bio: string | null
  company: string | null
  location: string | null
  avatar_url: string | null
  html_url: string | null
  followers: number
  following: number
  public_repos: number
}

export interface LanguageUsage {
  language: string
  count: number
}

export interface RepoPRs {
  repository: string
  count: number
}

export interface MonthlyContributionItem {
  month: string
  pull_requests: number
  issues: number
  commits: number
}

export interface HourlyActivityItem {
  period: string
  count: number
}

export interface SummaryStats {
  total_repos: number
  total_prs_merged: number
  merge_rate: number
}

export interface RecentEventItem {
  timestamp: string
  description: string
  event_type: string
}

export interface GitHubUserInsightsResponse {
  user_profile: UserProfile | null
  most_used_languages: LanguageUsage[]
  repos_with_more_prs: RepoPRs[]
  monthly_contributions: MonthlyContributionItem[]
  hours_more_activity: HourlyActivityItem[]
  summary_stats: SummaryStats | null
  recent_events: RecentEventItem[]
}
