from fastapi import FastAPI

from app.api.user.endpoints import router


def add_endpoints(app: FastAPI) -> FastAPI:
    app.include_router(router)

    return app
