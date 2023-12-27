import re
from typing import Callable, Iterable, Type

from httpx import Response
from pydantic import BaseModel

ResponseAsserter = Callable[[Response], Response]


RESPONSE_CONTENT_MUST_BE_LIST = (
    "{request_info} :: response content must be list\n{content}"
)
RESPONSE_CONTENT_MUST_BE_VALID_MODEL = (
    "{request_info} :: response content must be valid {model}\n{content}"
)


def get_request_info(response: Response) -> str:
    return f"{response.request.method} {response.request.url} {response.status_code}"


def json_model_is(
    model: Type[BaseModel],
    is_list: bool = False,
) -> ResponseAsserter:
    def _asserter(response: Response) -> Response:
        request_info = get_request_info(response)
        data = response.json()

        if is_list:
            assert isinstance(data, list), RESPONSE_CONTENT_MUST_BE_LIST.format(
                request_info=request_info,
                content=response.content,
            )

            for item in data:
                try:
                    model.model_validate(item)
                except Exception as exc:
                    raise AssertionError(
                        RESPONSE_CONTENT_MUST_BE_VALID_MODEL.format(
                            request_info=request_info,
                            model=model.__name__,
                            content=item,
                        )
                    ) from exc
        else:
            try:
                data = model.model_validate(data)
            except Exception as exc:
                raise AssertionError(
                    RESPONSE_CONTENT_MUST_BE_VALID_MODEL.format(
                        request_info=request_info,
                        model=model.__name__,
                        content=data,
                    )
                ) from exc
        return response

    return _asserter


RESPONSE_MUST_HAVE_HEADER = (
    "{request_info} :: response must have header {header}\n{content}"
)
RESPONSE_HEADER_MUST_SATISFY_REGEX = (
    "{request_info} :: response header {name}={value}"
    " must satisfy {target} regex\n{content}"
)
RESPONSE_HEADER_MUST_BE_EQUAL_TO_VALUE = (
    "{request_info} :: response header {name}={value}"
    " must be equal to {target} value\n{content}"
)


def has_header(
    name: str, value: str | None = None, regex: bool = False
) -> ResponseAsserter:
    def _asserter(response: Response) -> Response:
        request_info = get_request_info(response)

        assert name in response.headers, RESPONSE_MUST_HAVE_HEADER.format(
            request_info=request_info,
            header=name,
            content=response.content,
        )

        if value:
            if regex:
                assert (
                    re.search(value, response.headers[name]) is not None
                ), RESPONSE_HEADER_MUST_SATISFY_REGEX.format(
                    request_info=request_info,
                    name=name,
                    value=response.headers[name],
                    target=value,
                    content=response.content,
                )
            else:
                assert (
                    response.headers[name] == value
                ), RESPONSE_HEADER_MUST_BE_EQUAL_TO_VALUE.format(
                    request_info=request_info,
                    name=name,
                    value=response.headers[name],
                    target=value,
                    content=response.content,
                )

        return response

    return _asserter


RESPONSE_STATUS_CODE_MUST_BE = "{request_info} status code must be {target}\n{content}"
RESPONSE_STATUS_CODE_MUST_BE_ONE_OF = (
    "{request_info} status code must be one of{target}\n{content}"
)


def status_code_is(status_code: int | Iterable[int]) -> ResponseAsserter:
    def _asserter(response: Response) -> Response:
        request_info = get_request_info(response)
        if isinstance(status_code, Iterable):
            assert (
                response.status_code in status_code
            ), RESPONSE_STATUS_CODE_MUST_BE_ONE_OF.format(
                request_info=request_info,
                target=status_code,
                content=response.content,
            )
        else:
            assert (
                response.status_code == status_code
            ), RESPONSE_STATUS_CODE_MUST_BE.format(
                request_info=request_info,
                target=status_code,
                content=response.content,
            )

        return response

    return _asserter


RESPONSE_ERROR_LACKS_FIELD = "{request_info} error lacks {field}"
RESPONSE_ERROR_CODE_MISMATCH = (
    "{request_info} error code mismatch: target={target}, got={got}"
)


def json_is_error(
    must_have_meta: bool = True,
    error_code: str | None = None,
) -> ResponseAsserter:
    def _asserter(response: Response) -> Response:
        request_info = get_request_info(response)

        response_body = response.json()
        assert "errorMessage" in response_body, RESPONSE_ERROR_LACKS_FIELD.format(
            request_info=request_info,
            field="errorMessage",
        )

        assert "errorCode" in response_body, RESPONSE_ERROR_LACKS_FIELD.format(
            request_info=request_info,
            field="errorCode",
        )

        assert (
            "meta" in response_body if must_have_meta else True
        ), RESPONSE_ERROR_LACKS_FIELD.format(
            request_info=request_info,
            field="meta",
        )

        assert (
            response_body["errorCode"] == error_code if error_code else True
        ), RESPONSE_ERROR_CODE_MISMATCH.format(
            request_info=request_info,
            target=error_code,
            got=response_body["errorCode"],
        )

        return response

    return _asserter
