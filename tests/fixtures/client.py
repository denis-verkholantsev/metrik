import asyncio

import edgedb
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Client

from app.api.dependencies import edgedb_async_client, edgedb_config
from app.asgi import create


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
        yield loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()


def override_edgedb_client():
    config = edgedb_config()
    return edgedb.create_async_client(
        dsn=config.DSN,
        tls_security=config.TLS_SECURITY,
    )


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create()
    app.dependency_overrides[edgedb_async_client] = override_edgedb_client
    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> Client:
    return TestClient(
        app,
        raise_server_exceptions=True,
    )


@pytest.fixture(scope="session")
def edgedb_client():
    config = edgedb_config()
    client = edgedb.create_client(dsn=config.DSN, tls_security=config.TLS_SECURITY)

    yield client

    client.close()
