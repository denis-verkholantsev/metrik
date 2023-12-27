from http import HTTPStatus

from toolz import pipe

from app.api.user.contracts import BearerTokenResponse
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


def test_user_login(
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
):
    _response = metrik_api.post_user_login(
        fake_user.entity.info.username,
        fake_user.entity.info.password.get_secret_value(),
    )

    pipe(
        _response,
        response.status_code_is(HTTPStatus.OK),
        response.json_model_is(BearerTokenResponse),
    )


def test_user_login_not_found(
    metrik_api: MetrikAPI,
):
    _response = metrik_api.post_user_login("random_username", "random_password")

    pipe(
        _response,
        response.status_code_is(HTTPStatus.NOT_FOUND),
        response.json_is_error(must_have_meta=True),
    )
