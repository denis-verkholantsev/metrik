from typing import Annotated
from uuid import UUID

from caseconverter import camelcase
from fastapi import Body, Depends, Query
from pydantic import BaseModel

from app.api.common.contracts import SerializableUUID
from app.core.tree.models import Coordinates, SkillEntity, SkillInfo, SkillInfoUpdate


class PostSkillRequest(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    name: str
    description: str | None = None
    tree: UUID
    position: Coordinates

    def to_skill_info(self, author: UUID) -> SkillInfo:
        return SkillInfo(
            name=self.name,
            description=self.description,
            tree=self.tree,
            position=self.position,
            author=author,
        )


class SkillEntityResponse(BaseModel, alias_generator=camelcase, populate_by_name=True):
    uid: SerializableUUID
    name: str
    description: str | None = None
    tree: SerializableUUID
    author: SerializableUUID
    position: Coordinates

    @staticmethod
    def from_skill_entity(entity: SkillEntity) -> "SkillEntityResponse":
        return SkillEntityResponse(
            uid=entity.uid,
            name=entity.info.name,
            description=entity.info.description,
            tree=entity.info.tree,
            author=entity.info.author,
            position=entity.info.position,
        )


class SkillFilter(BaseModel):
    tree: UUID

    @staticmethod
    def from_query(tree: Annotated[UUID, Query()]) -> "SkillFilter":
        return SkillFilter(tree=tree)


class EmptyResponse(BaseModel):
    pass


class PutSkillRequest(BaseModel):
    name: str
    description: str | None
    position: Coordinates

    def to_skill_info_update(self) -> SkillInfoUpdate:
        return SkillInfoUpdate(**self.model_dump())


PutSkillRequestBody = Annotated[PutSkillRequest, Body()]
SkillFilterQuery = Annotated[SkillFilter, Depends(SkillFilter.from_query)]
PostSkillRequestBody = Annotated[PostSkillRequest, Body()]
