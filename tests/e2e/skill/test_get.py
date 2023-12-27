from http import HTTPStatus

import pytest
from toolz import pipe

from app.api.skill.contracts import PostSkillRequest, SkillEntityResponse, SkillFilter
from app.api.tree.contracts import PostSkillTreeRequest, SkillTreeEntityResponse
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


@pytest.mark.parametrize(
    ("body_tree", "body_skill"),
    [
        (
            {"name": "test_tree", "public": True},
            {"name": "test_skill", "position": {"x": 0, "y": 0}},
        ),
        (
            {"name": "test_tree", "public": False},
            {"name": "test_skill", "position": {"x": 0, "y": 0}},
        ),
    ],
)
def test_get_skills_public_tree(
    body_tree: dict,
    body_skill: dict,
    fake_user: FakeUser,
    another_fake_user: FakeUser,
    metrik_api: MetrikAPI,
):
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.post_tree(PostSkillTreeRequest(**body_tree))

    pipe(
        _response,
        response.status_code_is(HTTPStatus.CREATED),
        response.json_model_is(SkillTreeEntityResponse),
    )

    _response_body = _response.json()
    tree_uid = _response_body["uid"]
    body_skill["tree"] = tree_uid

    with metrik_api.with_user(fake_user) as _metrik_api:
        for _ in range(5):
            pipe(
                _metrik_api.post_skill(PostSkillRequest(**body_skill)),
                response.status_code_is(HTTPStatus.CREATED),
                response.json_model_is(SkillEntityResponse),
            )

    with metrik_api.with_user(fake_user) as _metrik_api:
        _response_my = _metrik_api.get_skill(SkillFilter(tree=tree_uid))

    pipe(
        _response_my,
        response.status_code_is(HTTPStatus.OK),
        response.json_model_is(SkillEntityResponse, is_list=True),
    )

    with metrik_api.with_user(another_fake_user) as _metrik_api:
        _response_another = _metrik_api.get_skill(SkillFilter(tree=tree_uid))

    pipe(
        _response_another,
        response.status_code_is(HTTPStatus.OK),
        response.json_model_is(SkillEntityResponse, is_list=True),
    )

    if body_tree.get("public"):
        assert (
            _response_my.content == _response_another.content
        ), "Sets of skills differ from user to another user"
    else:
        assert (
            len(
                [
                    SkillEntityResponse.model_validate(item)
                    for item in _response_another.json()
                ]
            )
            == 0
        ), "Set of private tree's skills are available for another user"
