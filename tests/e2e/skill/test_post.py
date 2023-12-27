from http import HTTPStatus

import pytest
from toolz import pipe

from app.api.skill.contracts import PostSkillRequest, SkillEntityResponse
from app.api.tree.contracts import SkillTreeEntityResponse
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


@pytest.mark.parametrize(
    "body_skill",
    [{"name": "test_skill", "position": {"x": 0, "y": 0}}],
)
def test_post_skill(
    body_skill: dict,
    fake_tree: SkillTreeEntityResponse,
    fake_user: FakeUser,
    another_fake_user: FakeUser,
    metrik_api: MetrikAPI,
):
    body_skill["tree"] = str(fake_tree.uid)

    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.post_skill(PostSkillRequest(**body_skill))

    pipe(
        _response,
        response.status_code_is(HTTPStatus.CREATED),
        response.json_model_is(SkillEntityResponse),
    )

    with metrik_api.with_user(another_fake_user) as _metrik_api:
        _response = _metrik_api.post_skill(PostSkillRequest(**body_skill))

    pipe(
        _response,
        response.status_code_is(HTTPStatus.NOT_FOUND),
        response.json_is_error(error_code="SkillTreeNotFound"),
    )
