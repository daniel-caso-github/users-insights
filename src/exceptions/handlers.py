from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from src.config.logger_config import get_logger

logger = get_logger("API_ERRORS")


def add_exception_handlers(app: FastAPI):
    """
    Adds global exception handlers to the FastAPI application.

    This function captures HTTP errors and unexpected server errors, logging them
    appropriately before returning a standardized JSON response.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Handles HTTP exceptions raised within the application.

        Logs the error details and returns a structured JSON response.

        Args:
            request (Request): The incoming HTTP request.
            exc (HTTPException): The exception raised.

        Returns:
            JSONResponse: A structured response with the appropriate status code.
        """
        logger.error(f"❌ HTTP {exc.status_code}: {exc.detail} - {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "status_code": exc.status_code},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Handles unexpected exceptions that are not explicitly caught.

        Logs the error details and returns a standardized internal server error response.

        Args:
            request (Request): The incoming HTTP request.
            exc (Exception): The unexpected exception.

        Returns:
            JSONResponse: A generic error response with status code 500.
        """
        logger.critical(f"🚨 Unexpected error at {request.url}: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "status_code": 500},
        )
