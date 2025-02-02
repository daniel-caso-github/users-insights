import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch
from main import app

client = TestClient(app)

mock_github_data = {
    "most_used_languages": [
        {"language": "Python", "count": 10},
        {"language": "JavaScript", "count": 5},
    ],
    "repos_with_more_prs": [
        {"repository": "https://github.com/user/repo1", "count": 3},
        {"repository": "https://github.com/user/repo2", "count": 2},
    ],
    "monthly_contributions": [
        {"month": "2025-02", "pull_requests": 2, "issues": 3, "commits": 10},
        {"month": "2025-01", "pull_requests": 1, "issues": 1, "commits": 5},
    ],
    "hours_more_activity": [
        {"period": "morning", "count": 5},
        {"period": "afternoon", "count": 8},
        {"period": "evening", "count": 12},
    ],
}
mock_user_not_found = {"message": "Not Found"}


@pytest.fixture
def mock_github_requests():
    with patch("services.github_client.request_with_rate_limit") as mock_request:
        mock_request.side_effect = lambda path: (
            mock_github_data
            if "users/torvalds" in path
            else mock_user_not_found if "users/usuario_no_existe" in path else None
        )
        yield mock_request


def test_get_insights_success(mock_github_requests):
    response = client.get("/user-insights/torvalds")
    assert response.status_code == status.HTTP_200_OK


#
def test_get_insights_user_not_found(mock_github_requests):
    response = client.get("/user-insights/usuario_no_existe")
    assert response.status_code == status.HTTP_404_NOT_FOUND
