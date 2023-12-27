from typing import Annotated
from uuid import UUID

from caseconverter import camelcase
from fastapi import Body, Depends, Query
from pydantic import BaseModel

from app.api.common.contracts import SerializableUUID
from app.core.tree.models import KnowledgeEntity, KnowledgeInfo, KnowledgeInfoUpdate


class PostKnowledgeRequest(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    name: str
    content: str
    skill: UUID

    def to_knowledge_info(self, author: UUID) -> KnowledgeInfo:
        return KnowledgeInfo(
            name=self.name, content=self.content, skill=self.skill, author=author
        )


class KnowledgeEntityResponse(
    BaseModel, alias_generator=camelcase, populate_by_name=True
):
    uid: SerializableUUID
    name: str
    content: str
    skill: SerializableUUID
    author: SerializableUUID

    @staticmethod
    def from_knowledge_entity(entity: KnowledgeEntity) -> "KnowledgeEntityResponse":
        return KnowledgeEntityResponse(
            uid=entity.uid,
            name=entity.info.name,
            content=entity.info.content,
            skill=entity.info.skill,
            author=entity.info.author,
        )


class KnowledgeFilter(BaseModel):
    skill: UUID

    @staticmethod
    def from_query(skill: Annotated[UUID, Query()]) -> "KnowledgeFilter":
        return KnowledgeFilter(skill=skill)


class PutKnowledgeRequest(BaseModel):
    name: str
    content: str

    def to_knowledge_info_update(self) -> KnowledgeInfoUpdate:
        return KnowledgeInfoUpdate(**self.model_dump())


class EmptyResponse(BaseModel):
    pass


KnowledgeFilterQuery = Annotated[KnowledgeFilter, Depends(KnowledgeFilter.from_query)]
PostKnowledgeRequestBody = Annotated[PostKnowledgeRequest, Body()]
PutKnowledgeRequestBody = Annotated[PutKnowledgeRequest, Body()]
