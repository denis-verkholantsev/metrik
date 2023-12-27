from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import RequestAuthorDependency, SkillRepositoryDependency
from app.api.skill.contracts import (
    EmptyResponse,
    PostSkillRequestBody,
    PutSkillRequestBody,
    SkillEntityResponse,
    SkillFilterQuery,
)
from app.core.tree.errors import SkillNotFoundError, SkillTreeNotFoundError
from app.core.tree.models import SkillEntity

router = APIRouter(prefix="/skill", tags=["skill"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=SkillEntityResponse
)
async def post_skill(
    body: PostSkillRequestBody,
    skill_repository: SkillRepositoryDependency,
    request_author: RequestAuthorDependency,
) -> SkillEntityResponse:
    info = body.to_skill_info(request_author)

    entity = await skill_repository.insert_one(info)

    if not entity:
        raise SkillTreeNotFoundError()

    return SkillEntityResponse.from_skill_entity(entity)


@router.put("/{skill_uid}", status_code=status.HTTP_200_OK)
async def put_skill(
    skill_uid: UUID,
    request_author: RequestAuthorDependency,
    skill_repository: SkillRepositoryDependency,
    body: PutSkillRequestBody,
):
    uid = await skill_repository.update_one_info(
        skill_uid=skill_uid, author=request_author, update=body.to_skill_info_update()
    )

    if not uid:
        raise SkillNotFoundError()


@router.get("", status_code=status.HTTP_200_OK)
async def get_skill(
    skill_filter: SkillFilterQuery,
    skill_repository: SkillRepositoryDependency,
    request_author: RequestAuthorDependency,
):
    entities = await skill_repository.select_many(
        tree_uid=skill_filter.tree, user_uid=request_author
    )

    if not entities:
        return []

    return [SkillEntityResponse.from_skill_entity(e) for e in entities]


@router.get(
    "/{skill_uid}", status_code=status.HTTP_200_OK, response_model=SkillEntityResponse
)
async def select_skill(
    skill_uid: UUID,
    skill_repository: SkillRepositoryDependency,
    request_author: RequestAuthorDependency,
) -> SkillEntityResponse:
    entity: SkillEntity | None = await skill_repository.select_one(
        skill_uid, request_author
    )

    if entity is None:
        raise SkillNotFoundError()

    return SkillEntityResponse.from_skill_entity(entity)


@router.delete(
    "/{skill_uid}", status_code=status.HTTP_200_OK, response_model=EmptyResponse
)
async def delete_skill(
    skill_uid: UUID,
    skill_repository: SkillRepositoryDependency,
    request_author: RequestAuthorDependency,
) -> EmptyResponse:
    await skill_repository.delete_one(skill_uid, request_author)
    return EmptyResponse()
