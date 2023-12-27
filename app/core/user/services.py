from typing import Protocol
from uuid import UUID

from pydantic import EmailStr, SecretStr

from app.core.user.models import UserEntity, UserInfo, UserInfoUpdate


class PasswordHasherService(Protocol):
    def hash_password(self, password: SecretStr) -> SecretStr:
        raise NotImplementedError()

    def compare_passwords(
        self, input_password: SecretStr, original_password: SecretStr
    ) -> bool:
        raise NotImplementedError()


class UserRepository(Protocol):
    async def insert_one(
        self,
        info: UserInfo,
    ) -> UserEntity:
        raise NotImplementedError()

    async def select_one(
        self,
        email: EmailStr | None = None,
        username: str | None = None,
        uid: UUID | None = None,
    ) -> UserEntity | None:
        raise NotImplementedError()

    async def update_one_info(
        self,
        user_uid: UUID,
        update: UserInfoUpdate,
    ) -> UUID | None:
        raise NotImplementedError()

    async def update_one_password(
        self,
        user_uid: UUID,
        password: SecretStr,
    ) -> UUID | None:
        raise NotImplementedError()
