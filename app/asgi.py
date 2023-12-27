from fastapi import FastAPI
from toolz import pipe

from app.api import errors_handlers, knowledge, link, middleware, skill, tree, user
from app.api.config import APIConfig


def create() -> FastAPI:
    api_config = APIConfig()
    app = api_config.init_fastapi()

    return pipe(
        app,
        errors_handlers.add,
        middleware.add_metrics,
        middleware.add_cors(api_config),  # pylint: disable=E1120
        user.add_endpoints,
        tree.add_endpoints,
        skill.add_endpoints,
        link.add_endpoints,
        knowledge.add_endpoints,
    )
