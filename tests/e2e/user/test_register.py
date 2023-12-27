from http import HTTPStatus
from uuid import uuid4

import pytest
from toolz import pipe

from app.api.user.contracts import UserEntityResponseWithToken
from app.core.user.models import UserInfo
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


def test_register_success(
    user_info: UserInfo,
    metrik_api: MetrikAPI,
):
    _response = metrik_api.post_user_register(user_info)

    pipe(
        _response,
        response.status_code_is(HTTPStatus.CREATED),
        response.json_model_is(UserEntityResponseWithToken),
    )


@pytest.mark.parametrize(
    ("override_email", "override_username", "status_code"),
    [
        (True, False, HTTPStatus.BAD_REQUEST),
        (False, True, HTTPStatus.BAD_REQUEST),
        (False, False, HTTPStatus.BAD_REQUEST),
        (True, True, HTTPStatus.CREATED),
    ],
)
def test_register_with_same_email_or_username(
    metrik_api: MetrikAPI,
    fake_user: FakeUser,
    override_email: bool,
    override_username: bool,
    status_code: int,
):
    info = fake_user.entity.info

    # we consider that email already has uuid hex and replace it with another
    if override_email:
        info.email = uuid4().hex + info.email[32:]
    if override_username:
        info.username = uuid4().hex + info.username[32:]

    _response = metrik_api.post_user_register(info)

    pipe(
        _response,
        response.status_code_is(status_code),
    )
