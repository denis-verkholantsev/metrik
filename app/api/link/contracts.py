from typing import Annotated
from uuid import UUID

from caseconverter import camelcase
from fastapi import Body, Depends, Query
from pydantic import BaseModel

from app.api.common.contracts import SerializableUUID
from app.core.tree.models import SkillLinkInfo


class PostSkillLinkRequest(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    source: UUID
    target: UUID
    tree: UUID

    def to_skill_link_info(self) -> SkillLinkInfo:
        return SkillLinkInfo(**self.model_dump())


class SkillLinkResponse(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    source: SerializableUUID
    target: SerializableUUID


class SkillLinkFilter(BaseModel):
    tree: UUID

    @staticmethod
    def from_query(tree: Annotated[UUID, Query()]) -> "SkillLinkFilter":
        return SkillLinkFilter(tree=tree)


class DeleteSkillLinkFilter(BaseModel):
    source: UUID
    target: UUID
    tree: UUID

    @staticmethod
    def from_query(
        source: Annotated[UUID, Query()],
        target: Annotated[UUID, Query()],
        tree: Annotated[UUID, Query()],
    ) -> "DeleteSkillLinkFilter":
        return DeleteSkillLinkFilter(source=source, target=target, tree=tree)

    def to_skill_link_info(self) -> SkillLinkInfo:
        return SkillLinkInfo(**self.model_dump())


class EmptyResponse(BaseModel):
    pass


PostSkillLinkRequestBody = Annotated[PostSkillLinkRequest, Body()]
SkillLinkFilterQuery = Annotated[SkillLinkFilter, Depends(SkillLinkFilter.from_query)]
DeleteSkillLinkFilterQuery = Annotated[
    DeleteSkillLinkFilter, Depends(DeleteSkillLinkFilter.from_query)
]
