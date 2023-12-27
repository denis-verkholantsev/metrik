from http import HTTPStatus

from toolz import pipe

from app.api.user.contracts import UserEntityResponse
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


def test_user_get_me(
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
):
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.get_user_me()

    assert pipe(
        _response,
        response.status_code_is(HTTPStatus.OK),
        response.json_model_is(UserEntityResponse),
    )
