from fastapi import APIRouter, status

from app.api.dependencies import (
    RequestAuthorDependency,
    SkillLinkRepositoryDependency,
    SkillTreeRepositoryDependency,
)
from app.api.link.contracts import (
    DeleteSkillLinkFilterQuery,
    EmptyResponse,
    PostSkillLinkRequestBody,
    SkillLinkFilterQuery,
    SkillLinkResponse,
)
from app.core.tree.errors import SkillTreeNotFoundError

router = APIRouter(prefix="/link", tags=["link"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SkillLinkResponse,
)
async def post_link(
    body: PostSkillLinkRequestBody,
    skill_tree_repository: SkillTreeRepositoryDependency,
    skill_link_repository: SkillLinkRepositoryDependency,
    request_author: RequestAuthorDependency,
):
    tree = await skill_tree_repository.select_one(body.tree)

    if not tree or tree.info.author != request_author:
        raise SkillTreeNotFoundError()

    await skill_link_repository.insert_one(body.to_skill_link_info())

    return SkillLinkResponse(
        source=body.source,
        target=body.target,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[SkillLinkResponse],
)
async def get_link(
    query: SkillLinkFilterQuery,
    skill_link_repository: SkillLinkRepositoryDependency,
    request_author: RequestAuthorDependency,
):
    links = await skill_link_repository.select_many(
        tree_uid=query.tree,
        author_uid=request_author,
    )

    return [SkillLinkResponse(source=link.source, target=link.target) for link in links]


@router.delete("", status_code=status.HTTP_200_OK, response_model=None)
async def delete_link(
    query: DeleteSkillLinkFilterQuery,
    skill_link_repository: SkillLinkRepositoryDependency,
    request_author: RequestAuthorDependency,
):
    await skill_link_repository.delete_one(
        info=query.to_skill_link_info(), author=request_author
    )

    return EmptyResponse()
