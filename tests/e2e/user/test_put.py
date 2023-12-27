from http import HTTPStatus

import edgedb
import pytest
from toolz import pipe

from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FAKE_USER_PASSWORD, FakeUser


@pytest.mark.parametrize(
    ("update", "target_status"),
    [
        ({}, HTTPStatus.UNPROCESSABLE_ENTITY),
        (
            {
                "firstName": "Test First Name",
                "lastName": "Test Last Name",
                "birthdate": "2000-01-01",
                "description": "Test Description",
                "location": "Test Location",
                "occupance": "Test occupance",
            },
            HTTPStatus.OK,
        ),
    ],
)
def test_user_put(
    update: dict,
    target_status: int,
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
    edgedb_client: edgedb.Client,
):
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response_put = _metrik_api.put_user(update)

    pipe(
        _response_put,
        response.status_code_is(target_status),
    )

    if not _response_put.is_success:
        pipe(
            _response_put,
            response.json_is_error(),
        )
    else:
        result = edgedb_client.query_single(
            "select User { * } filter .id = <uuid>$uid",
            uid=fake_user.entity.uid,
        )

        assert result, "no user found in database!"
        assert update["firstName"] == result.first_name
        assert update["lastName"] == result.last_name
        assert update["birthdate"] == result.birthdate.strftime("%Y-%m-%d")
        assert update["description"] == result.description
        assert update["location"] == result.location
        assert update["occupance"] == result.occupance


def test_user_put_unauthorized(
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
):
    fake_user.token = ""

    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.put_user({})

    pipe(
        _response,
        response.status_code_is(HTTPStatus.UNAUTHORIZED),
        response.json_is_error(),
    )


@pytest.mark.parametrize(
    ("new_password", "old_password", "target_status", "error_code"),
    [
        ("newPassword", FAKE_USER_PASSWORD, HTTPStatus.OK, None),
        (
            FAKE_USER_PASSWORD,
            FAKE_USER_PASSWORD,
            HTTPStatus.BAD_REQUEST,
            "InvalidNewPassword",
        ),
        (
            "newPassword",
            "wrongOldPassword",
            HTTPStatus.UNAUTHORIZED,
            "UserPasswordMismatch",
        ),
    ],
)
def test_user_put_password(  # pylint: disable=R0913
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
    new_password: str,
    old_password: str,
    target_status: int,
    error_code: str | None,
):
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = _metrik_api.put_user_password(old_password, new_password)

    pipe(
        _response,
        response.status_code_is(target_status),
    )

    if not _response.is_success:
        pipe(
            _response,
            response.json_is_error(error_code=error_code),
        )
