from datetime import date
from typing import Annotated

from caseconverter import camelcase
from fastapi import Body
from pydantic import BaseModel, EmailStr, Field, SecretStr

from app.api.common.contracts import SerializableDate, SerializableUUID
from app.core.user.models import (
    UserEntity,
    UserInfo,
    UserInfoUpdate,
    UserPasswordUpdate,
)


class PostRegisterRequest(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    username: str
    first_name: str
    last_name: str
    birthdate: date | None = None
    email: EmailStr
    password: SecretStr

    def to_user_info(self) -> UserInfo:
        return UserInfo(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            birthdate=self.birthdate,
            email=self.email,
            password=self.password,
        )


class UserEntityResponse(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    uid: SerializableUUID
    username: str
    first_name: str
    last_name: str
    birthdate: SerializableDate | None = None
    email: EmailStr
    avatar_url: str | None = None
    description: str | None = None
    location: str | None = None
    occupance: str | None = None
    external_links: list[str] = Field(default_factory=list)

    @staticmethod
    def from_user_entity(entity: UserEntity) -> "UserEntityResponse":
        return UserEntityResponse(
            uid=entity.uid,
            **entity.info.model_dump(),
        )


class UserEntityResponseWithToken(
    UserEntityResponse,
    alias_generator=camelcase,
    populate_by_name=True,
):
    token: str
    token_type: str = "bearer"

    @staticmethod
    def from_user_entity_and_token(
        entity: UserEntity, token: str
    ) -> "UserEntityResponseWithToken":
        return UserEntityResponseWithToken(
            uid=entity.uid,
            token=token,
            **entity.info.model_dump(),
        )


class BearerTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UpdateUserInfoRequest(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    first_name: str
    last_name: str
    birthdate: SerializableDate | None = None
    description: str | None = None
    location: str | None = None
    occupance: str | None = None

    def to_user_info_update(self) -> UserInfoUpdate:
        return UserInfoUpdate(**self.model_dump())


class UpdateUserPasswordRequest(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    new_password: SecretStr
    old_password: SecretStr

    def to_user_password_update(self) -> UserPasswordUpdate:
        return UserPasswordUpdate(**self.model_dump())


PostRegisterRequestBody = Annotated[PostRegisterRequest, Body()]
UpdateUserRequestBody = Annotated[UpdateUserInfoRequest, Body()]
UpdateUserPasswordBody = Annotated[UpdateUserPasswordRequest, Body()]
