from contextlib import contextmanager
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Client, Response

from app.api.common.contracts import Pagination
from app.api.link.contracts import PostSkillLinkRequest, SkillLinkFilter
from app.api.skill.contracts import PostSkillRequest, SkillFilter
from app.api.tree.contracts import (
    PostSkillTreeRequest,
    PutSkillTreeRequest,
    SkillTreeFilter,
)
from app.core.user.models import UserInfo
from tests.fixtures.models import FakeUser


@dataclass(slots=True)
class MetrikAPI:  # pylint: disable=too-many-public-methods
    client: Client
    current_user: FakeUser | None = None

    @contextmanager
    def with_user(self, user: FakeUser):
        self.current_user = user
        yield self
        self.current_user = None

    def post_user_register(self, info: UserInfo) -> Response:
        return self.client.post(
            "/user/register",
            json={
                "username": info.username,
                "firstName": info.first_name,
                "lastName": info.last_name,
                "birthdate": info.birthdate.isoformat() if info.birthdate else None,
                "email": info.email,
                "password": info.password.get_secret_value(),
            },
        )

    def post_user_login(self, username: str, password: str) -> Response:
        return self.client.post(
            "/user/login",
            data={
                "username": username,
                "password": password,
            },
        )

    def put_user(self, update: dict) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.put(
            "/user",
            json=update,
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def get_user_me(self) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.get(
            "/user/me",
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def put_user_password(self, old_password: str, new_password: str):
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.put(
            "/user/password",
            json={
                "oldPassword": old_password,
                "newPassword": new_password,
            },
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def post_tree(self, request: PostSkillTreeRequest) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.post(
            "/tree",
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def get_tree(self, query: SkillTreeFilter, pagination: Pagination) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.get(
            "/tree",
            params={
                **{key: value for key, value in query.model_dump().items() if value},
                **{
                    key: value
                    for key, value in pagination.model_dump().items()
                    if value
                },
            },
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def put_tree(self, tree_uid: UUID, update: PutSkillTreeRequest) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.put(
            f"/tree/{tree_uid}",
            json=update.model_dump(),
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def get_tree_uid(self, uid: UUID) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.get(
            f"/tree/{uid}",
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def post_skill(self, body: PostSkillRequest) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.post(
            "/skill",
            content=body.model_dump_json(),
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def get_skill(self, query: SkillFilter) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"
        return self.client.get(
            "/skill",
            params={
                **{key: value for key, value in query.model_dump().items() if value}
            },
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def post_link(self, body: PostSkillLinkRequest) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.post(
            "/link",
            content=body.model_dump_json(),
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )

    def get_link(self, query: SkillLinkFilter) -> Response:
        assert (
            self.current_user
        ), "cannot perform authorized request as current user is None"

        return self.client.get(
            "/link",
            params={"tree": str(query.tree)},
            headers={"Authorization": f"Bearer {self.current_user.token}"},
        )


@pytest.fixture(scope="session")
def metrik_api(client: Client) -> MetrikAPI:
    return MetrikAPI(client)
