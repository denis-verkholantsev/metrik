from http import HTTPStatus
from uuid import uuid4

import edgedb
import pytest
from toolz import pipe

from app.api.tree.contracts import (
    PostSkillTreeRequest,
    PutSkillTreeRequest,
    SkillTreeEntityResponse,
)
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


@pytest.mark.parametrize(
    ("name", "description"),
    [
        ("another_name", None),
        ("another_name", "Lorem ipsum"),
    ],
)
def test_put_tree(
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
    edgedb_client: edgedb.Client,
    name: str,
    description: str | None,
):
    with metrik_api.with_user(fake_user):
        _response = metrik_api.post_tree(PostSkillTreeRequest(name="test"))

        pipe(
            _response,
            response.status_code_is(HTTPStatus.CREATED),
            response.json_model_is(SkillTreeEntityResponse),
        )

        fake_skill_tree = SkillTreeEntityResponse.model_validate(_response.json())

        _response = metrik_api.put_tree(
            fake_skill_tree.uid,
            PutSkillTreeRequest(
                name=name,
                description=description,
            ),
        )

    pipe(
        _response,
        response.status_code_is(HTTPStatus.OK),
    )

    result = edgedb_client.query_single(
        "select SkillTree { id, name, description } filter .id = <uuid>$uid",
        uid=fake_skill_tree.uid,
    )

    assert result, "SkillTree not found"
    assert result.name == name
    assert result.description == description


def test_put_not_authored(
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
):
    fake_tree_uid = uuid4()

    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.put_tree(
            fake_tree_uid, PutSkillTreeRequest(name="test", description="description")
        )

    pipe(
        _response,
        response.status_code_is(HTTPStatus.NOT_FOUND),
        response.json_is_error(error_code="SkillTreeNotFound"),
    )
