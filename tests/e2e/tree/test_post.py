from http import HTTPStatus

import edgedb
import pytest
from toolz import pipe

from app.api.tree.contracts import PostSkillTreeRequest, SkillTreeEntityResponse
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


@pytest.mark.parametrize(
    "body",
    [
        {"name": "test_tree"},
        {"name": "test_tree", "description": "test_description"},
        {"name": "test_tree", "public": True},
        {"name": "test_tree", "public_grades": True},
    ],
)
def test_tree_post(
    body: dict,
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
    edgedb_client: edgedb.Client,
):
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.post_tree(PostSkillTreeRequest(**body))

    pipe(
        _response,
        response.status_code_is(HTTPStatus.CREATED),
        response.json_model_is(SkillTreeEntityResponse),
    )

    _response_body = _response.json()

    result = edgedb_client.query_single(
        "select SkillTree {*} filter .id = <uuid>$uid", uid=_response_body["uid"]
    )

    assert result, "SkillTree not found in database"
    assert str(result.id) == _response_body["uid"]
    assert result.name == body["name"]
    assert result.description == body.get("description", None)
    assert result.public == body.get("public", False)
    assert result.public_grades == body.get("public_grades", False)
