from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import UUID

from authlib.jose import JsonWebToken
from pydantic import Field, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.common.errors import AppError
from app.core.user.models import UserEntity


class InvalidJWTSignatureError(AppError):
    error_message = "JWT has invalid jwt signature"


class InvalidJWTPayloadError(AppError):
    error_message = "invalid JWT payload: {reason}"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JWT_", frozen=True)

    ALGORITHM: Literal["HS256", "HS384", "HS512"] = Field(default="HS256")
    EXPIRES_MINUTES: PositiveInt = Field(default=1440)
    SECRET: SecretStr = Field(default="secret")


@dataclass
class JWTService:
    settings: JWTConfig
    jwt: JsonWebToken

    def __init__(self, settings: JWTConfig):
        self.settings = settings
        self.jwt = JsonWebToken([self.settings.ALGORITHM])

    def generate_token(self, user_entry: UserEntity) -> bytes:
        header: dict[str, Any] = {"alg": self.settings.ALGORITHM}
        payload: dict[str, Any] = {
            "sub": str(user_entry.uid),
            "exp": datetime.now(tz=timezone.utc)
            + timedelta(minutes=self.settings.EXPIRES_MINUTES),
        }

        # pylint: disable=E1101
        return self.jwt.encode(
            header,
            payload,
            self.settings.SECRET.get_secret_value(),
        )

    def decode_token(self, token: str) -> UUID:
        try:
            # pylint: disable=E1101
            claims = self.jwt.decode(
                token,
                key=self.settings.SECRET.get_secret_value(),
            )
        except Exception as err:
            raise InvalidJWTSignatureError() from err
        if "sub" not in claims:
            raise InvalidJWTPayloadError(reason="no sub")

        return UUID(claims.get("sub"))
