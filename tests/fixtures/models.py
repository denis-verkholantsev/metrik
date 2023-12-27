from dataclasses import dataclass
from http import HTTPStatus
from uuid import uuid4

import pytest
from faker import Faker
from pydantic import BaseModel
from toolz import pipe

from app.api.skill.contracts import PostSkillRequest, SkillEntityResponse
from app.api.tree.contracts import PostSkillTreeRequest, SkillTreeEntityResponse
from app.api.user.contracts import UserEntityResponseWithToken
from app.core.tree.models import Coordinates, SkillTreeInfo
from app.core.user.models import UserEntity, UserInfo
from tests.assertions import response

FAKE_USER_PASSWORD = "testPassword123"


@dataclass(slots=True)
class ModelFaker:
    faker: Faker

    def user_info(self) -> UserInfo:
        profile = self.faker.profile()
        first_name, *_, last_name = profile["name"].split(" ")
        return UserInfo(
            username=uuid4().hex + "-" + profile["username"],
            first_name=first_name,
            last_name=last_name,
            email=uuid4().hex + "-" + profile["mail"],
            birthdate=profile["birthdate"],
            password=FAKE_USER_PASSWORD,  # type: ignore
        )

    def user_entity(self) -> UserEntity:
        return UserEntity(
            uid=uuid4(),
            info=self.user_info(),
        )

    def skill_tree(self) -> SkillTreeInfo:
        public = self.faker.pybool()
        return SkillTreeInfo(
            name=self.faker.name(),
            public=public,
            public_grades=self.faker.pybool() if public else False,
            description=self.faker.text(),
            author=uuid4(),
        )


@pytest.fixture()
def model_faker(faker: Faker) -> ModelFaker:
    return ModelFaker(faker)


@pytest.fixture()
def user_info(model_faker: ModelFaker) -> UserInfo:
    return model_faker.user_info()


@pytest.fixture()
def user_entity(model_faker: ModelFaker) -> UserEntity:
    return model_faker.user_entity()


class FakeUser(BaseModel):
    entity: UserEntity
    token: str


@pytest.fixture()
def fake_user(
    model_faker: ModelFaker,
    metrik_api,
) -> FakeUser:
    info = model_faker.user_info()

    _response = pipe(
        metrik_api.post_user_register(info),
        response.status_code_is(HTTPStatus.CREATED),
        response.json_model_is(UserEntityResponseWithToken),
    )

    body = UserEntityResponseWithToken.model_validate(_response.json())
    entity = UserEntity(
        uid=body.uid,
        info=UserInfo(
            username=body.username,
            email=body.email,
            first_name=body.first_name,
            last_name=body.last_name,
            birthdate=body.birthdate,
            password=info.password,
            location=body.location,
            occupance=body.occupance,
            description=body.description,
            external_links=body.external_links,
            avatar_url=body.avatar_url,
        ),
    )

    return FakeUser(entity=entity, token=body.token)


@pytest.fixture()
def fake_tree(
    fake_user: FakeUser,
    metrik_api,
) -> SkillTreeEntityResponse:
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = pipe(
            _metrik_api.post_tree(
                PostSkillTreeRequest(name=str(uuid4()) + "-test-tree"),
            ),
            response.status_code_is(HTTPStatus.CREATED),
            response.json_model_is(SkillTreeEntityResponse),
        )

    return SkillTreeEntityResponse.model_validate(_response.json())


@pytest.fixture()
def fake_skill(
    fake_user: FakeUser,
    fake_tree: SkillTreeEntityResponse,
    metrik_api,
) -> SkillEntityResponse:
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = pipe(
            _metrik_api.post_skill(
                PostSkillRequest(
                    name=str(uuid4()) + "-test-tree",
                    tree=fake_tree.uid,
                    position=Coordinates(x=0, y=0),
                ),
            ),
            response.status_code_is(HTTPStatus.CREATED),
            response.json_model_is(SkillEntityResponse),
        )

    return SkillEntityResponse.model_validate(_response.json())


another_fake_user = fake_user
another_fake_tree = fake_tree
another_fake_skill = fake_skill
