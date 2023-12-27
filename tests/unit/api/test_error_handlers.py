import json
from http import HTTPStatus

import pytest
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.errors_handlers import (
    ModelValidationError,
    _handle_app_error,
    _handle_exception,
    _handle_http_exception,
    _handle_request_validation_error,
)
from app.core.user.errors import (
    UserDuplicateEmailOrUsernameError,
    UserNotFoundError,
    UserPasswordMismatchError,
)
from app.service.security.jwt import InvalidJWTPayloadError, InvalidJWTSignatureError


@pytest.mark.parametrize(
    ("error", "response_status", "error_handler", "has_meta"),
    [
        (
            InvalidJWTPayloadError(reason="test"),
            HTTPStatus.UNAUTHORIZED,
            _handle_app_error,
            True,
        ),
        (InvalidJWTSignatureError(), HTTPStatus.UNAUTHORIZED, _handle_app_error, True),
        (
            ModelValidationError(),
            HTTPStatus.UNPROCESSABLE_ENTITY,
            _handle_app_error,
            True,
        ),
        (UserNotFoundError(), HTTPStatus.NOT_FOUND, _handle_app_error, True),
        (UserPasswordMismatchError(), HTTPStatus.UNAUTHORIZED, _handle_app_error, True),
        (
            UserDuplicateEmailOrUsernameError(),
            HTTPStatus.BAD_REQUEST,
            _handle_app_error,
            True,
        ),
        (
            HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="test_detail"),
            HTTPStatus.BAD_REQUEST,
            _handle_http_exception,
            False,
        ),
        (
            RequestValidationError(errors=[]),
            HTTPStatus.UNPROCESSABLE_ENTITY,
            _handle_request_validation_error,
            True,
        ),
        (
            Exception("test exception"),
            HTTPStatus.INTERNAL_SERVER_ERROR,
            _handle_exception,
            False,
        ),
    ],
)
def test_error_handlers(
    error,
    error_handler,
    response_status,
    has_meta,
):
    response = error_handler(object(), error)

    assert isinstance(response, JSONResponse)
    assert response.status_code == response_status

    response_dict = json.loads(response.body)
    assert "errorMessage" in response_dict
    assert "errorCode" in response_dict
    assert "meta" in response_dict if has_meta else True
