from fastapi import FastAPI, Depends

from schermas.github_insights import GitHubUserInsightsResponse
from services.github_insights_service import GitHubInsightsService

app = FastAPI(
    title="GitHub User Insights API",
    description=(
        "An API that analyzes GitHub users' activity using advanced metrics, "
        "including language usage, most active repositories, monthly contributions, "
        "and activity hours."
    ),
    version="1.0.0",
)


@app.get(
    "/user-insights/{username}",
    summary="Retrieve GitHub user insights",
    description=(
        "Returns analytics on a GitHub user's activity, including the most used programming languages, "
        "repositories with the most pull requests, monthly contribution breakdown, and the user's most active hours."
    ),
    response_model=GitHubUserInsightsResponse,
    responses={
        200: {"description": "Successfully retrieved insights"},
        404: {"description": "GitHub user not found"},
        500: {"description": "Internal server error"},
    },
)
def get_insights_user(username: str, service: GitHubInsightsService = Depends()):
    """
    Fetches detailed insights on a given GitHub user's activity.

    Args:
        username (str): The GitHub username to retrieve insights for.
        service (GitHubInsightsService, optional): Dependency injection of the GitHub insights service.

    Returns:
        GitHubUserInsightsResponse: A structured response with analytics data.
    """
    return service.get_data(username)
