from http import HTTPStatus

import pytest
from toolz import pipe

from app.api.common.contracts import Pagination
from app.api.tree.contracts import (
    PostSkillTreeRequest,
    SkillTreeEntityResponse,
    SkillTreeFilter,
)
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser, ModelFaker


@pytest.mark.parametrize(
    ("public", "name"),
    [
        (None, None),
        (True, None),
        (False, None),
        (None, "name"),
        (True, "name"),
        (False, "name"),
    ],
)
def test_get_tree_many(  # pylint: disable=too-many-arguments,too-many-statements
    model_faker: ModelFaker,
    fake_user: FakeUser,
    another_fake_user: FakeUser,
    metrik_api: MetrikAPI,
    public: bool | None,
    name: str | None,
):
    fake_user_skill_trees: list[SkillTreeEntityResponse] = []

    with metrik_api.with_user(fake_user) as _metrik_api:
        for i in range(5):
            fake_tree = model_faker.skill_tree()
            _response = _metrik_api.post_tree(
                PostSkillTreeRequest(
                    name=name if i == 0 and name else fake_tree.name,
                    description=fake_tree.description,
                    public=fake_tree.public,
                    public_grades=fake_tree.public_grades,
                )
            )

            pipe(
                _response,
                response.status_code_is(HTTPStatus.CREATED),
                response.json_model_is(SkillTreeEntityResponse),
            )

            entity = SkillTreeEntityResponse.model_validate(_response.json())

            fake_user_skill_trees.append(entity)

    another_fake_user_skill_trees: list[SkillTreeEntityResponse] = []

    with metrik_api.with_user(another_fake_user) as _metrik_api:
        for i in range(5):
            fake_tree = model_faker.skill_tree()
            _response = _metrik_api.post_tree(
                PostSkillTreeRequest(
                    name=name if i == 0 and name else fake_tree.name,
                    description=fake_tree.description,
                    public=fake_tree.public,
                    public_grades=fake_tree.public_grades,
                )
            )

            pipe(
                _response,
                response.status_code_is(HTTPStatus.CREATED),
                response.json_model_is(SkillTreeEntityResponse),
            )

            entity = SkillTreeEntityResponse.model_validate(_response.json())

            another_fake_user_skill_trees.append(entity)

    with metrik_api.with_user(fake_user) as _metrik_api:
        _response_my = _metrik_api.get_tree(
            SkillTreeFilter(public=public, name=name), Pagination(page=0, per_page=10)
        )

        _response_another = _metrik_api.get_tree(
            SkillTreeFilter(
                author=another_fake_user.entity.uid, public=public, name=name
            ),
            Pagination(page=0, per_page=10),
        )

    pipe(
        _response_my,
        response.status_code_is(HTTPStatus.OK),
        response.json_model_is(SkillTreeEntityResponse, is_list=True),
    )
    pipe(
        _response_another,
        response.status_code_is(HTTPStatus.OK),
        response.json_model_is(SkillTreeEntityResponse, is_list=True),
    )

    _response_my_json = _response_my.json()
    result_my_skill_tree_entities = {
        e.uid: e
        for e in [SkillTreeEntityResponse.model_validate(r) for r in _response_my_json]
    }

    _response_another_json = _response_another.json()
    result_another_skill_tree_entities = {
        e.uid: e
        for e in [
            SkillTreeEntityResponse.model_validate(r) for r in _response_another_json
        ]
    }

    target_my_filtered_skill_trees = [
        t
        for t in fake_user_skill_trees
        if (True if public is not None and t.public == public else not public)
        and (True if name and name in t.name else not name)
    ]

    for target in target_my_filtered_skill_trees:
        result = result_my_skill_tree_entities.get(target.uid)

        assert result, f"failed to get my skill tree entity with uid: {target.uid}"
        assert result == target, "result and target entities are not the same"

    target_another_filtered_skill_trees = [
        t
        for t in another_fake_user_skill_trees
        if t.public and (True if name and name in t.name else not name)
    ]

    for target in target_another_filtered_skill_trees:
        result = result_another_skill_tree_entities.get(target.uid)

        assert result, (
            f"failed to get another skill tree entity with uid: {target.uid}, "
            f"publicity: {target.public}"
        )
        assert result == target, "result and target entities are not the same"


def test_get_tree_one(
    fake_user: FakeUser,
    another_fake_user: FakeUser,
    metrik_api: MetrikAPI,
    model_faker: ModelFaker,
):
    tree_name = "my_test_tree"

    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.post_tree(PostSkillTreeRequest(name=tree_name))

        pipe(
            _response,
            response.status_code_is(HTTPStatus.CREATED),
            response.json_model_is(SkillTreeEntityResponse),
        )

        target = SkillTreeEntityResponse.model_validate(_response.json())

        _response = _metrik_api.get_tree_uid(target.uid)

        pipe(
            _response,
            response.status_code_is(HTTPStatus.OK),
            response.json_model_is(SkillTreeEntityResponse),
        )

        result = SkillTreeEntityResponse.model_validate(_response.json())

        assert result.name == target.name
        assert result.description == target.description
        assert result.public == target.public
        assert result.public_grades == target.public_grades

    with metrik_api.with_user(another_fake_user) as _metrik_api:
        pipe(
            _metrik_api.get_tree_uid(target.uid),
            response.status_code_is(HTTPStatus.NOT_FOUND),
            response.json_is_error(error_code="SkillTreeNotFound"),
        )
