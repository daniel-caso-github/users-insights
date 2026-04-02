# Backend — GitHub User Insights API

REST API built with FastAPI that returns activity metrics for a GitHub user.

## Installation

```bash
# Instalar dependencias (prod)
uv sync

# Instalar incluyendo dev
uv sync --group dev
```

## Environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable               | Description                                      | Default                    |
|------------------------|--------------------------------------------------|----------------------------|
| `GITHUB_TOKEN`         | GitHub Personal Access Token (required)          | —                          |
| `GITHUB_API_URL`       | GitHub API base URL                              | `https://api.github.com`   |
| `MAX_RESULTS_PER_PAGE` | Results per page for pagination                  | `100`                      |
| `MAX_PAGES`            | Maximum number of pages to traverse             | `5`                        |

### Generate a GitHub Token

1. Go to [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new)
2. Set a name and expiration date
3. Select scopes: `read:user`, `read:org`, `public_repo`
4. Copy the generated token into `.env`

## Run the API

```bash
uv run uvicorn main:app --reload
```

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Docker

```bash
# All services
docker-compose up --build

# Backend only
docker-compose up --build backend
```

API available at `http://localhost:8000`.

## Endpoint

```
GET /user-insights/{username}
```

### Successful response (200)

```json
{
  "user_profile": {
    "name": "Jane Doe",
    "bio": "Software engineer",
    "company": "Acme Inc.",
    "location": "Buenos Aires",
    "avatar_url": "https://avatars.githubusercontent.com/u/1",
    "html_url": "https://github.com/janedoe",
    "followers": 42,
    "following": 10,
    "public_repos": 15
  },
  "most_used_languages": [
    {"language": "Python", "count": 10},
    {"language": "JavaScript", "count": 5}
  ],
  "repos_with_more_prs": [
    {"repository": "https://github.com/user/repo1", "count": 3}
  ],
  "monthly_contributions": [
    {"month": "2025-02", "pull_requests": 2, "issues": 3, "commits": 10}
  ],
  "hours_more_activity": [
    {"period": "morning", "count": 5},
    {"period": "afternoon", "count": 8},
    {"period": "evening", "count": 12}
  ],
  "summary_stats": {
    "total_repos": 15,
    "total_prs_merged": 47,
    "merge_rate": 85
  },
  "recent_events": [
    {"timestamp": "2025-02-10T14:23:00Z", "description": "Opened PR in user/repo1", "event_type": "PullRequestEvent"},
    {"timestamp": "2025-02-09T09:00:00Z", "description": "Pushed to user/repo2", "event_type": "PushEvent"}
  ]
}
```

### Response codes

| Code | Description                    |
|------|--------------------------------|
| 200  | Data retrieved successfully    |
| 404  | GitHub user not found          |
| 500  | Internal server error          |

## Tests

```bash
uv run pytest tests/

# With detailed output
uv run pytest tests/ -v
```

## Architecture

```
main.py (FastAPI router + DI)
    └─ GitHubInsightsService  (src/services/github_insights_service.py)
           ├─ GitHubAPIService  (src/services/github_client_service.py)
           └─ Metrics (src/services/metrics/*.py)
```

### Metrics pattern

Each metric inherits from `BaseGitHubMetric` and implements `execute(username) -> dict`. The orchestrator discovers them dynamically via `pkgutil.iter_modules()` and runs them according to their `order` attribute.

To add a new metric: create a file in `src/services/metrics/` with a class that inherits from `BaseGitHubMetric`, defines `order: int` and implements `execute`.
