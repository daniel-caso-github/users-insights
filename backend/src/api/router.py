from fastapi import APIRouter, Depends

from opt.constans.tags import Tags
from opt.schemas.github_insights import GitHubUserInsightsResponse
from src.services.github_insights_service import GitHubInsightsService

router = APIRouter()


@router.get(
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
    tags=[Tags.users],
)
async def get_insights_user(username: str, service: GitHubInsightsService = Depends()):
    return await service.execute(username)
