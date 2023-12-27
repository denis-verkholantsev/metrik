from http import HTTPStatus

import edgedb
from toolz import pipe

from app.api.link.contracts import PostSkillLinkRequest, SkillLinkResponse
from app.api.skill.contracts import SkillEntityResponse
from app.api.tree.contracts import SkillTreeEntityResponse
from app.core.tree.models import SkillLinkInfo
from tests.assertions import response
from tests.fixtures.api import MetrikAPI
from tests.fixtures.models import FakeUser


def test_post_link(  # pylint: disable=too-many-arguments
    fake_user: FakeUser,
    fake_tree: SkillTreeEntityResponse,
    fake_skill: SkillEntityResponse,
    another_fake_skill: SkillEntityResponse,
    edgedb_client: edgedb.Client,
    metrik_api: MetrikAPI,
):
    with metrik_api.with_user(fake_user) as _metrik_api:
        _response = pipe(
            _metrik_api.post_link(
                PostSkillLinkRequest(
                    source=fake_skill.uid,
                    target=another_fake_skill.uid,
                    tree=fake_tree.uid,
                )
            ),
            response.status_code_is(HTTPStatus.CREATED),
            response.json_model_is(SkillLinkResponse),
        )

    skill_link = SkillLinkResponse.model_validate(_response.json())

    target = edgedb_client.query(
        "select Skill {id, contains} filter .tree.id = <uuid>$tree",
        tree=fake_tree.uid,
    )

    def _to_skill_links(obj) -> list[SkillLinkInfo]:
        return [
            SkillLinkInfo(source=obj.id, target=x.id, tree=fake_tree.uid)
            for x in obj.contains
        ]

    target = [skill_link for t in target for skill_link in _to_skill_links(t)]

    assert len(target) == 1
    assert target[0].source == skill_link.source
    assert target[0].target == skill_link.target
