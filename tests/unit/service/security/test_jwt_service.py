import pytest

from app.core.user.models import UserEntity
from app.service.security.jwt import JWTConfig, JWTService


@pytest.fixture(scope="module")
def jwt_service() -> JWTService:
    config = JWTConfig(
        ALGORITHM="HS256",
        EXPIRES_MINUTES=30,
        SECRET="test_secret",  # type: ignore
    )

    return JWTService(config)


def test_jwt_service_generate_and_decode(
    jwt_service: JWTService,
    user_entity: UserEntity,
) -> None:
    token = jwt_service.generate_token(user_entity)

    user_uid = jwt_service.decode_token(token.decode())

    assert user_uid == user_entity.uid, "failed to decode JWT"
