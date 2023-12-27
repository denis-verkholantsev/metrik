from dataclasses import dataclass
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic import EmailStr, SecretStr

from app.core.user.errors import (
    InvalidSelectUserQueryParametersError,
    UserDuplicateEmailOrUsernameError,
)
from app.core.user.models import UserEntity, UserInfo, UserInfoUpdate
from app.core.user.services import UserRepository
from scripts import (
    insert_user,
    select_user_filter_email,
    select_user_filter_uid,
    select_user_filter_username,
    update_user_info,
    update_user_password,
)


@dataclass
class EdgeDBUserRepository(UserRepository):
    executor: AsyncIOExecutor

    async def insert_one(self, info: UserInfo) -> UserEntity:
        result = await insert_user(
            executor=self.executor,
            username=info.username,
            first_name=info.first_name,
            last_name=info.last_name,
            birthdate=info.birthdate,
            email=info.email,
            password=info.password.get_secret_value(),
        )

        if result is None:
            raise UserDuplicateEmailOrUsernameError()

        return UserEntity(
            uid=result.id,
            info=info,
        )

    async def select_one(
        self,
        email: EmailStr | None = None,
        username: str | None = None,
        uid: UUID | None = None,
    ) -> UserEntity | None:
        match (email, username, uid):
            case (str() as some_email, None, None):
                result = await select_user_filter_email(
                    self.executor,
                    email=some_email,
                )
            case (None, str() as some_username, None):
                result = await select_user_filter_username(
                    self.executor,
                    username=some_username,
                )
            case (None, None, UUID() as some_uid):
                result = await select_user_filter_uid(
                    self.executor,
                    uid=some_uid,
                )
            case _:
                raise InvalidSelectUserQueryParametersError()

        if not result:
            return None

        return UserEntity(
            uid=result.id,
            info=UserInfo(
                username=result.username,
                first_name=result.first_name,
                last_name=result.last_name,
                birthdate=result.birthdate,
                email=result.email,
                avatar_url=result.avatar_url,
                description=result.description,
                location=result.location,
                occupance=result.occupance,
                external_links=[link.url for link in result.external_links],
                password=SecretStr(result.password),
            ),
        )

    async def update_one_info(
        self,
        user_uid: UUID,
        update: UserInfoUpdate,
    ) -> UUID | None:
        result = await update_user_info(
            self.executor,
            uid=user_uid,
            first_name=update.first_name,
            last_name=update.last_name,
            birthdate=update.birthdate,
            description=update.description,
            location=update.location,
            occupance=update.occupance,
        )

        if not result:
            return None

        return result.id

    async def update_one_password(
        self, user_uid: UUID, password: SecretStr
    ) -> UUID | None:
        result = await update_user_password(
            self.executor,
            uid=user_uid,
            password=password.get_secret_value(),
        )

        if not result:
            return None

        return result.id
