from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import router
from src.config.logger_config import setup_logging
from src.exceptions.handlers import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="GitHub User Insights API",
        description=(
            "An API that analyzes GitHub users' activity using advanced metrics, "
            "including language usage, most active repositories, monthly contributions, "
            "and activity hours."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    app.include_router(router)
    add_exception_handlers(app)

    return app
