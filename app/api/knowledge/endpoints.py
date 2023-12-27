from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import KnowledgeRepositoryDependency, RequestAuthorDependency
from app.api.knowledge.contracts import (
    EmptyResponse,
    KnowledgeEntityResponse,
    KnowledgeFilterQuery,
    PostKnowledgeRequestBody,
    PutKnowledgeRequestBody,
)
from app.core.tree.errors import KnowledgeNotFoundError, SkillNotFoundError
from app.core.tree.models import KnowledgeEntity, KnowledgeInfo

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=KnowledgeEntityResponse
)
async def post_knowledge(
    body: PostKnowledgeRequestBody,
    knowledge_repository: KnowledgeRepositoryDependency,
    request_author: RequestAuthorDependency,
) -> KnowledgeEntityResponse:
    info: KnowledgeInfo = body.to_knowledge_info(request_author)

    entity: KnowledgeEntity | None = await knowledge_repository.insert_one(info)

    if not entity:
        raise SkillNotFoundError()

    return KnowledgeEntityResponse.from_knowledge_entity(entity)


@router.get("", status_code=status.HTTP_200_OK)
async def get_knowledge(
    knowledge_filter: KnowledgeFilterQuery,
    knowledge_repository: KnowledgeRepositoryDependency,
    request_author: RequestAuthorDependency,
) -> list[KnowledgeEntityResponse]:
    entities: list[KnowledgeEntity] = await knowledge_repository.select_many(
        skill_uid=knowledge_filter.skill, user_uid=request_author
    )

    return [KnowledgeEntityResponse.from_knowledge_entity(e) for e in entities]


@router.put("/{uid}", status_code=status.HTTP_200_OK, response_model=EmptyResponse)
async def put_knowledge(
    uid: UUID,
    request_author: RequestAuthorDependency,
    knowledge_repository: KnowledgeRepositoryDependency,
    body: PutKnowledgeRequestBody,
) -> EmptyResponse:
    result_uid: UUID | None = await knowledge_repository.update_one_info(
        knowledge_uid=uid,
        author_uid=request_author,
        update=body.to_knowledge_info_update(),
    )

    if not result_uid:
        raise KnowledgeNotFoundError()

    return EmptyResponse()


@router.delete("/{uid}", status_code=status.HTTP_200_OK, response_model=EmptyResponse)
async def delete_knowledge(
    uid: UUID,
    knowledge_repository: KnowledgeRepositoryDependency,
    request_author: RequestAuthorDependency,
) -> EmptyResponse:
    await knowledge_repository.delete_one(uid, request_author)
    return EmptyResponse()
