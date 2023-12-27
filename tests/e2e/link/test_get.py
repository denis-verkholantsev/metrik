from http import HTTPStatus

from httpx import Response
from toolz import curried, pipe

from app.api.link.contracts import (
    PostSkillLinkRequest,
    SkillLinkFilter,
    SkillLinkResponse,
)
from app.api.skill.contracts import SkillEntityResponse
from app.api.tree.contracts import SkillTreeEntityResponse
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


def test_get_link(
    fake_user: FakeUser,
    metrik_api: MetrikAPI,
    fake_tree: SkillTreeEntityResponse,
    fake_skill: SkillEntityResponse,
    another_fake_skill: SkillEntityResponse,
):
    with metrik_api.with_user(fake_user) as _metrik_api:
        skill_link: SkillLinkResponse = pipe(
            _metrik_api.post_link(
                PostSkillLinkRequest(
                    source=fake_skill.uid,
                    target=another_fake_skill.uid,
                    tree=fake_tree.uid,
                )
            ),
            response.status_code_is(HTTPStatus.CREATED),
            response.json_model_is(SkillLinkResponse),
            Response.json,
            SkillLinkResponse.model_validate,
        )  # type: ignore

        skill_links: list[SkillLinkResponse] = pipe(
            _metrik_api.get_link(SkillLinkFilter(tree=fake_tree.uid)),
            response.status_code_is(HTTPStatus.OK),
            response.json_model_is(SkillLinkResponse, is_list=True),
            Response.json,
            curried.map(SkillLinkResponse.model_validate),
            list,
        )  # type: ignore

    assert len(skill_links) == 1
    assert skill_links[0] == skill_link
