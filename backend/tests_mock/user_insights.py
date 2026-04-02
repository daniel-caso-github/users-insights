import random

mock_github_data = {
    "torvalds": {
        "name": "Linus Torvalds",
        "bio": "Linux creator",
        "company": None,
        "location": "Portland, OR",
        "avatar_url": "https://avatars.githubusercontent.com/u/1024025",
        "html_url": "https://github.com/torvalds",
        "followers": 236000,
        "following": 0,
        "public_repos": 10,
        "search_prs_total": {"total_count": 50},
        "search_prs_merged": {"total_count": 40},
        "events": [
            {
                "type": "PushEvent",
                "repo": {"name": "torvalds/linux"},
                "payload": {},
                "created_at": "2025-01-01T10:00:00Z",
            },
            {
                "type": "PullRequestEvent",
                "repo": {"name": "torvalds/linux"},
                "payload": {"action": "opened"},
                "created_at": "2025-01-02T11:00:00Z",
            },
        ],
        "most_used_languages": [
            {"language": "Python", "count": random.randint(5000, 50000)},
            {"language": "JavaScript", "count": random.randint(1000, 20000)},
            {"language": "Rust", "count": random.randint(500, 5000)},
        ],
        "repos_with_more_prs": [
            {
                "repository": "https://api.github.com/repos/alice/data-science",
                "count": random.randint(10, 50),
            },
            {
                "repository": "https://api.github.com/repos/alice/web-app",
                "count": random.randint(5, 20),
            },
        ],
        "monthly_contributions": [
            {
                "month": "2025-02",
                "pull_requests": random.randint(0, 5),
                "issues": random.randint(0, 10),
                "commits": random.randint(50, 300),
            },
            {
                "month": "2025-01",
                "pull_requests": random.randint(0, 5),
                "issues": random.randint(0, 10),
                "commits": random.randint(50, 300),
            },
        ],
        "hours_more_activity": [
            {"period": "morning", "count": random.randint(10, 30)},
            {"period": "afternoon", "count": random.randint(20, 50)},
            {"period": "evening", "count": random.randint(30, 70)},
        ],
    },
    "dhh": {
        "name": "David Heinemeier Hansson",
        "bio": "Rails creator",
        "company": "37signals",
        "location": "Malibu, CA",
        "avatar_url": "https://avatars.githubusercontent.com/u/2741",
        "html_url": "https://github.com/dhh",
        "followers": 15000,
        "following": 50,
        "public_repos": 25,
        "search_prs_total": {"total_count": 120},
        "search_prs_merged": {"total_count": 100},
        "events": [
            {
                "type": "WatchEvent",
                "repo": {"name": "rails/rails"},
                "payload": {},
                "created_at": "2025-01-03T09:00:00Z",
            },
        ],
        "most_used_languages": [
            {"language": "Go", "count": random.randint(5000, 30000)},
            {"language": "Kotlin", "count": random.randint(2000, 15000)},
        ],
        "repos_with_more_prs": [
            {
                "repository": "https://api.github.com/repos/bob/mobile-app",
                "count": random.randint(10, 40),
            },
            {
                "repository": "https://api.github.com/repos/bob/backend-service",
                "count": random.randint(5, 20),
            },
        ],
        "monthly_contributions": [
            {
                "month": "2025-02",
                "pull_requests": random.randint(0, 3),
                "issues": random.randint(0, 8),
                "commits": random.randint(20, 200),
            },
        ],
        "hours_more_activity": [
            {"period": "morning", "count": random.randint(5, 25)},
            {"period": "afternoon", "count": random.randint(10, 40)},
            {"period": "evening", "count": random.randint(20, 60)},
        ],
    },
    "tenderlove": {
        "name": "Aaron Patterson",
        "bio": "Ruby and Rails core",
        "company": "Shopify",
        "location": "Seattle, WA",
        "avatar_url": "https://avatars.githubusercontent.com/u/3124",
        "html_url": "https://github.com/tenderlove",
        "followers": 8000,
        "following": 200,
        "public_repos": 80,
        "search_prs_total": {"total_count": 300},
        "search_prs_merged": {"total_count": 270},
        "events": [
            {
                "type": "ForkEvent",
                "repo": {"name": "ruby/ruby"},
                "payload": {},
                "created_at": "2025-01-04T14:00:00Z",
            },
        ],
        "most_used_languages": [
            {"language": "C#", "count": random.randint(3000, 20000)},
            {"language": "PHP", "count": random.randint(1000, 12000)},
            {"language": "Ruby", "count": random.randint(500, 7000)},
        ],
        "repos_with_more_prs": [
            {
                "repository": "https://api.github.com/repos/charlie/game-engine",
                "count": random.randint(10, 50),
            },
            {
                "repository": "https://api.github.com/repos/charlie/ecommerce",
                "count": random.randint(5, 25),
            },
        ],
        "monthly_contributions": [
            {
                "month": "2025-02",
                "pull_requests": random.randint(0, 2),
                "issues": random.randint(0, 5),
                "commits": random.randint(30, 150),
            },
        ],
        "hours_more_activity": [
            {"period": "morning", "count": random.randint(8, 20)},
            {"period": "afternoon", "count": random.randint(15, 35)},
            {"period": "evening", "count": random.randint(25, 50)},
        ],
    },
    "mojombo": {
        "name": "Tom Preston-Werner",
        "bio": "GitHub co-founder",
        "company": None,
        "location": "San Francisco, CA",
        "avatar_url": "https://avatars.githubusercontent.com/u/1",
        "html_url": "https://github.com/mojombo",
        "followers": 22000,
        "following": 11,
        "public_repos": 62,
        "search_prs_total": {"total_count": 80},
        "search_prs_merged": {"total_count": 60},
        "events": [
            {
                "type": "CreateEvent",
                "repo": {"name": "mojombo/grit"},
                "payload": {"ref_type": "branch"},
                "created_at": "2025-01-05T16:00:00Z",
            },
        ],
        "most_used_languages": [
            {"language": "Swift", "count": random.randint(2000, 10000)},
            {"language": "TypeScript", "count": random.randint(1000, 8000)},
        ],
        "repos_with_more_prs": [
            {
                "repository": "https://api.github.com/repos/diana/ios-app",
                "count": random.randint(10, 30),
            },
            {
                "repository": "https://api.github.com/repos/diana/frontend",
                "count": random.randint(5, 15),
            },
        ],
        "monthly_contributions": [
            {
                "month": "2025-02",
                "pull_requests": random.randint(0, 4),
                "issues": random.randint(0, 6),
                "commits": random.randint(15, 100),
            },
        ],
        "hours_more_activity": [
            {"period": "morning", "count": random.randint(6, 18)},
            {"period": "afternoon", "count": random.randint(12, 30)},
            {"period": "evening", "count": random.randint(20, 40)},
        ],
    },
}
