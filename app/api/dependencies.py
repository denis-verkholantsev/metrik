from __future__ import annotations

from typing import Annotated
from uuid import UUID

import edgedb
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.tree.services import (
    KnowledgeRepository,
    SkillLinkRepository,
    SkillRepository,
    SkillTreeRepository,
)
from app.core.user.services import PasswordHasherService, UserRepository
from app.service.edgedb.config import EdgeDBConfig
from app.service.edgedb.knowledge import EdgeDBKnowledgeRepository
from app.service.edgedb.link import EdgeDBSkillLinkRepository
from app.service.edgedb.skill import EdgeDBSkillRepository
from app.service.edgedb.tree import EdgeDBSkillTreeRepository
from app.service.edgedb.user import EdgeDBUserRepository
from app.service.security.jwt import JWTConfig, JWTService
from app.service.security.password import PasslibPasswordHasherService

__edgedb_config: EdgeDBConfig | None = None
__edgedb_client: edgedb.AsyncIOClient | None = None
__jwt_config: JWTConfig | None = None
__jwt_service: JWTService | None = None
__oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def edgedb_config() -> EdgeDBConfig:
    # pylint: disable=global-statement
    global __edgedb_config

    if not __edgedb_config:
        __edgedb_config = EdgeDBConfig()

    return __edgedb_config  # noqa


def edgedb_async_client(config: EdgeDBConfigDependency) -> edgedb.AsyncIOClient:
    # pylint: disable=global-statement
    global __edgedb_client

    if not __edgedb_client:
        __edgedb_client = edgedb.create_async_client(
            dsn=config.DSN,
            tls_security=config.TLS_SECURITY,
        )

    return __edgedb_client  # noqa


async def edgedb_async_executor(client: EdgeDBAsyncClientDependency):
    async for tx in client.transaction():
        async with tx:
            yield tx


def user_repository(executor: EdgeDBAsyncExecutorDependency) -> UserRepository:
    return EdgeDBUserRepository(executor=executor)


def skill_tree_repository(
    executor: EdgeDBAsyncExecutorDependency,
) -> SkillTreeRepository:
    return EdgeDBSkillTreeRepository(executor=executor)


def skill_repository(
    executor: EdgeDBAsyncExecutorDependency,
) -> SkillRepository:
    return EdgeDBSkillRepository(executor=executor)


def skill_link_repository(
    executor: EdgeDBAsyncExecutorDependency,
) -> SkillLinkRepository:
    return EdgeDBSkillLinkRepository(executor)


def knowledge_repository(
    executor: EdgeDBAsyncExecutorDependency,
) -> EdgeDBKnowledgeRepository:
    return EdgeDBKnowledgeRepository(executor=executor)


def jwt_config() -> JWTConfig:
    # pylint: disable=global-statement
    global __jwt_config

    if not __jwt_config:
        __jwt_config = JWTConfig()

    return __jwt_config  # noqa


def jwt_service(jwt_config: JWTConfigDependency) -> JWTService:
    # pylint: disable=global-statement
    global __jwt_service

    if not __jwt_service:
        __jwt_service = JWTService(jwt_config)

    return __jwt_service  # noqa


def request_author(
    token: JWTAuthHeader,
    jwt_service: JWTServiceDependency,
) -> UUID:
    return jwt_service.decode_token(token)


def password_hasher_service() -> PasswordHasherService:
    return PasslibPasswordHasherService()


EdgeDBConfigDependency = Annotated[
    EdgeDBConfig,
    Depends(edgedb_config),
]
EdgeDBAsyncClientDependency = Annotated[
    edgedb.AsyncIOClient,
    Depends(edgedb_async_client),
]
EdgeDBAsyncExecutorDependency = Annotated[
    edgedb.AsyncIOExecutor,
    Depends(edgedb_async_executor, use_cache=True),
]
JWTConfigDependency = Annotated[
    JWTConfig,
    Depends(jwt_config),
]
JWTServiceDependency = Annotated[
    JWTService,
    Depends(jwt_service),
]
JWTAuthHeader = Annotated[
    str,
    Depends(__oauth2_scheme),
]
RequestAuthorDependency = Annotated[
    UUID,
    Depends(request_author),
]
UserRepositoryDependency = Annotated[
    UserRepository,
    Depends(user_repository),
]
SkillTreeRepositoryDependency = Annotated[
    SkillTreeRepository,
    Depends(skill_tree_repository),
]
SkillRepositoryDependency = Annotated[
    SkillRepository,
    Depends(skill_repository),
]
SkillLinkRepositoryDependency = Annotated[
    SkillLinkRepository,
    Depends(skill_link_repository),
]
KnowledgeRepositoryDependency = Annotated[
    KnowledgeRepository,
    Depends(knowledge_repository),
]
PasswordHasherServiceDependency = Annotated[
    PasswordHasherService,
    Depends(password_hasher_service),
]
OAuth2PasswordRequestFormDependency = Annotated[
    OAuth2PasswordRequestForm,
    Depends(),
]
