from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from toolz import curry

from app.api.config import APIConfig


def add_metrics(app: FastAPI) -> FastAPI:
    Instrumentator().instrument(app).expose(
        app,
        include_in_schema=False,
    )

    return app


@curry
def add_cors(config: APIConfig, app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ALLOW_ORIGINS,
        allow_credentials=config.CORS_ALLOW_CREDENTIALS,
        allow_methods=config.CORS_ALLOW_METHODS,
        allow_headers=config.CORS_ALLOW_ORIGINS,
    )

    return app
