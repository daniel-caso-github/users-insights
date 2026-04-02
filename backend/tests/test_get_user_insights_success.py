import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch
from main import app
from src.services.github_client_service import GitHubAPIService
from tests_mock.user_insights import mock_github_data

client = TestClient(app)


@pytest.fixture
def mock_github_requests():
    with patch.object(GitHubAPIService, "request_with_rate_limit") as mock_request:
        def mock_api_response(path):
            path_parts = path.split("/")
            if "users" in path_parts and len(path_parts) > path_parts.index("users") + 1:
                username = path_parts[path_parts.index("users") + 1]
                return mock_github_data.get(username, {"message": "Not Found"})
            return {"message": "Not Found"}

        mock_request.side_effect = mock_api_response
        yield mock_request


@pytest.mark.parametrize("username", ["torvalds", "dhh", "tenderlove", "mojombo"])
def test_get_insights_success(mock_github_requests, username):
    response = client.get(f"/user-insights/{username}")

    assert response.status_code == status.HTTP_200_OK

    print(f"Test passed for {username}")