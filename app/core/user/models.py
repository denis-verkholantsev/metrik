from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserInfo(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    birthdate: date | None = None
    avatar_url: str | None = None
    description: str | None = None
    location: str | None = None
    occupance: str | None = None
    external_links: list[str] = Field(default_factory=list)
    password: SecretStr


class UserEntity(BaseModel):
    uid: UUID
    info: UserInfo


class UserInfoUpdate(BaseModel):
    first_name: str
    last_name: str
    birthdate: date | None
    description: str | None
    location: str | None
    occupance: str | None


class UserPasswordUpdate(BaseModel):
    old_password: SecretStr
    new_password: SecretStr
