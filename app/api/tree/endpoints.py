from uuid import UUID

from fastapi import APIRouter, status

from app.api.common.contracts import PaginationQuery
from app.api.dependencies import RequestAuthorDependency, SkillTreeRepositoryDependency
from app.api.link.contracts import EmptyResponse
from app.api.tree.contracts import (
    PostSkillTreeRequestBody,
    PutSkillTreeRequestBody,
    SkillTreeEntityResponse,
    SkillTreeFilterQuery,
)
from app.core.tree.errors import SkillTreeNotFoundError
from app.core.tree.models import SkillTreeQuery

router = APIRouter(prefix="/tree", tags=["tree"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SkillTreeEntityResponse,
)
async def post_tree(
    body: PostSkillTreeRequestBody,
    skill_tree_repository: SkillTreeRepositoryDependency,
    request_author: RequestAuthorDependency,
) -> SkillTreeEntityResponse:
    info = body.to_skill_tree_info(request_author)

    entity = await skill_tree_repository.insert_one(info)

    return SkillTreeEntityResponse.from_skill_tree_entity(entity)


@router.get("")
async def get_tree(
    pagination: PaginationQuery,
    tree_filter: SkillTreeFilterQuery,
    skill_tree_repository: SkillTreeRepositoryDependency,
    request_author: RequestAuthorDependency,
):
    query = SkillTreeQuery(
        author=tree_filter.author or request_author,
        public=True
        if tree_filter.author and tree_filter != request_author
        else tree_filter.public,
        name=tree_filter.name,
    )

    entities = await skill_tree_repository.select_many(
        query,
        page=pagination.page,
        per_page=pagination.per_page,
    )

    return [SkillTreeEntityResponse.from_skill_tree_entity(e) for e in entities]


@router.put(
    "/{tree_uid}",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def put_tree(
    tree_uid: UUID,
    body: PutSkillTreeRequestBody,
    request_author: RequestAuthorDependency,
    skill_tree_repository: SkillTreeRepositoryDependency,
):
    uid = await skill_tree_repository.update_one_info(
        tree_uid, request_author, body.to_skill_tree_info_update()
    )

    if uid is None:
        raise SkillTreeNotFoundError()


@router.get(
    "/{uid}",
    status_code=status.HTTP_200_OK,
    response_model=SkillTreeEntityResponse,
)
async def get_tree_uid(
    uid: UUID,
    request_author: RequestAuthorDependency,
    skill_tree_repository: SkillTreeRepositoryDependency,
):
    entity = await skill_tree_repository.select_one(uid)

    if not entity or entity.info.author != request_author:
        raise SkillTreeNotFoundError()

    return SkillTreeEntityResponse.from_skill_tree_entity(entity)


@router.post(
    "/{uid}/like",
    status_code=status.HTTP_200_OK,
    response_model=EmptyResponse,
)
async def add_like_in_tree(
    uid: UUID,
    request_author: RequestAuthorDependency,
    skill_tree_repository: SkillTreeRepositoryDependency,
):
    status: bool = await skill_tree_repository.add_like(uid, request_author)
    if not status:
        raise SkillTreeNotFoundError()


@router.delete(
    "/{uid}/like",
    status_code=status.HTTP_200_OK,
    response_model=EmptyResponse,
)
async def remove_like(
    uid: UUID,
    request_author: RequestAuthorDependency,
    skill_tree_repository: SkillTreeRepositoryDependency,
):
    status: bool = await skill_tree_repository.remove_like(uid, request_author)

    if not status:
        raise SkillTreeNotFoundError()

    return EmptyResponse()
