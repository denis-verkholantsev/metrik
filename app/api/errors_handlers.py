from typing import Type

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.common.errors import AppError
from app.core.tree.errors import (
    KnowledgeNotFoundError,
    SkillNotFoundError,
    SkillTreeNotFoundError,
)
from app.core.user.errors import (
    InvalidNewPasswordError,
    UserDuplicateEmailOrUsernameError,
    UserNotFoundError,
    UserPasswordMismatchError,
)
from app.service.security.jwt import InvalidJWTPayloadError, InvalidJWTSignatureError


class ModelValidationError(AppError):
    error_message = "validation error"


ERROR_TO_STATUS_CODE: dict[Type[AppError], int] = {
    InvalidJWTPayloadError: status.HTTP_401_UNAUTHORIZED,
    InvalidJWTSignatureError: status.HTTP_401_UNAUTHORIZED,
    ModelValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    UserPasswordMismatchError: status.HTTP_401_UNAUTHORIZED,
    UserDuplicateEmailOrUsernameError: status.HTTP_400_BAD_REQUEST,
    InvalidNewPasswordError: status.HTTP_400_BAD_REQUEST,
    SkillTreeNotFoundError: status.HTTP_404_NOT_FOUND,
    SkillNotFoundError: status.HTTP_404_NOT_FOUND,
    KnowledgeNotFoundError: status.HTTP_404_NOT_FOUND,
}


def _handle_app_error(_: Request, err: AppError) -> Response:
    # TODO: add warning log if AppError type has no mapping to status code
    status_code = ERROR_TO_STATUS_CODE.get(
        type(err),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        content={
            "errorMessage": err.error_message,
            "errorCode": err.error_code,
            "meta": err.meta,
        },
        status_code=status_code,
    )


def _handle_http_exception(_: Request, err: HTTPException) -> Response:
    return JSONResponse(
        content={"errorMessage": err.detail, "errorCode": "HTTP"},
        status_code=err.status_code,
    )


def _handle_request_validation_error(
    request: Request, err: RequestValidationError
) -> Response:
    validation_error = ModelValidationError(errors=err.errors())
    return _handle_app_error(request, validation_error)


def _handle_validation_error(request: Request, err: ValidationError) -> Response:
    validation_error = ModelValidationError(errors=err.errors())
    return _handle_app_error(request, validation_error)


def _handle_exception(_: Request, err: Exception) -> Response:
    return JSONResponse(
        content={
            "errorMessage": str(err),
            "errorCode": "UnhandledError",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def add(app: FastAPI) -> FastAPI:
    app.add_exception_handler(AppError, _handle_app_error)
    app.add_exception_handler(RequestValidationError, _handle_request_validation_error)
    app.add_exception_handler(ValidationError, _handle_validation_error)
    app.add_exception_handler(HTTPException, _handle_http_exception)
    app.add_exception_handler(Exception, _handle_exception)
    return app
