from datetime import datetime
from typing import Any
from uuid import uuid4

import pytest

from app.core.user.errors import InvalidSelectUserQueryParametersError
from app.service.edgedb.user import EdgeDBUserRepository
from scripts import SelectUserFilterEmailResult


@pytest.fixture()
def user_repository(mocker):
    return EdgeDBUserRepository(object())  # type: ignore


@pytest.fixture()
def select_user_filter_result():
    return SelectUserFilterEmailResult(
        id=uuid4(),
        username="test_username",
        email="test_email@email.ru",
        first_name="test_first_name",
        last_name="test_last_name",
        password="",
        created=datetime.now(),
        birthdate=None,
        modified=None,
        location=None,
        description=None,
        avatar_url=None,
        occupance=None,
        external_links=[],
    )


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "query",
    [
        {},
        {"email": "test_email", "username": "test_username"},
        {"email": "test_email", "uid": uuid4()},
        {"uid": uuid4(), "username": "test_username"},
    ],
)
async def test_select_user_no_arguments_raises_exception(
    monkeypatch,
    user_repository: EdgeDBUserRepository,
    query: dict[str, Any],
):
    invoked_script = False

    async def mock_select_script(*_, **__):
        nonlocal invoked_script
        invoked_script = True

    monkeypatch.setattr(
        "app.service.edgedb.user.select_user_filter_email",
        mock_select_script,
    )
    monkeypatch.setattr(
        "app.service.edgedb.user.select_user_filter_uid",
        mock_select_script,
    )
    monkeypatch.setattr(
        "app.service.edgedb.user.select_user_filter_username",
        mock_select_script,
    )

    with pytest.raises(InvalidSelectUserQueryParametersError):
        await user_repository.select_one(**query)

    assert invoked_script is False


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "query",
    [
        {"email": "test_email"},
        {"username": "test_username"},
        {"uid": uuid4()},
    ],
)
async def test_select_user_argument_matching(
    monkeypatch,
    select_user_filter_result,
    user_repository: EdgeDBUserRepository,
    query: dict[str, Any],
):
    invoked_script = False

    async def mock_select_script(*_, **__):
        nonlocal invoked_script
        invoked_script = True
        return select_user_filter_result

    monkeypatch.setattr(
        "app.service.edgedb.user.select_user_filter_email",
        mock_select_script,
    )
    monkeypatch.setattr(
        "app.service.edgedb.user.select_user_filter_uid",
        mock_select_script,
    )
    monkeypatch.setattr(
        "app.service.edgedb.user.select_user_filter_username",
        mock_select_script,
    )

    await user_repository.select_one(**query)

    assert invoked_script is True
