import re

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch, AsyncMock
from main import app
from src.services.github_client_service import GitHubAPIService
from tests_mock.user_insights import mock_github_data

client = TestClient(app)


@pytest.fixture
def mock_github_requests():
    with patch.object(GitHubAPIService, "request_with_rate_limit", new_callable=AsyncMock) as mock_request:
        async def mock_api_response(path, client):
            if path.startswith("/search/issues"):
                match = re.search(r"author:(\w+)", path)
                if not match:
                    return {"total_count": 0, "items": []}
                username = match.group(1)
                user_data = mock_github_data.get(username, {})
                if "is:merged" in path:
                    return user_data.get("search_prs_merged", {"total_count": 0})
                return user_data.get("search_prs_total", {"total_count": 0})

            path_parts = path.split("/")
            if "users" in path_parts and len(path_parts) > path_parts.index("users") + 1:
                username = path_parts[path_parts.index("users") + 1].split("?")[0]
                user_data = mock_github_data.get(username, {"message": "Not Found"})

                if "events" in path_parts:
                    return user_data.get("events", [])

                return user_data

            return {"message": "Not Found"}

        mock_request.side_effect = mock_api_response
        yield mock_request


@pytest.mark.parametrize("username", ["torvalds", "dhh", "tenderlove", "mojombo"])
def test_get_insights_success(mock_github_requests, username):
    response = client.get(f"/user-insights/{username}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "user_profile" in data
    profile = data["user_profile"]
    assert "followers" in profile
    assert "following" in profile
    assert "public_repos" in profile

    assert "summary_stats" in data
    stats = data["summary_stats"]
    assert "total_repos" in stats
    assert "total_prs_merged" in stats
    assert "merge_rate" in stats

    assert "recent_events" in data
    events = data["recent_events"]
    assert isinstance(events, list)
    assert len(events) > 0
    event = events[0]
    assert "timestamp" in event
    assert "description" in event
    assert "event_type" in event

    print(f"Test passed for {username}")
