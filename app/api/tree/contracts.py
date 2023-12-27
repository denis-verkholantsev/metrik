from typing import Annotated
from uuid import UUID

from caseconverter import camelcase
from fastapi import Body, Depends, Query
from pydantic import BaseModel

from app.api.common.contracts import SerializableUUID
from app.core.tree.models import SkillTreeEntity, SkillTreeInfo, SkillTreeInfoUpdate


class PostSkillTreeRequest(
    BaseModel,
    alias_generator=camelcase,
    populate_by_name=True,
):
    name: str
    description: str | None = None
    public: bool = False
    public_grades: bool = False

    def to_skill_tree_info(self, author: UUID) -> SkillTreeInfo:
        return SkillTreeInfo(
            name=self.name,
            description=self.description,
            public=self.public,
            public_grades=self.public_grades,
            author=author,
        )


class SkillTreeEntityResponse(
    BaseModel, alias_generator=camelcase, populate_by_name=True
):
    uid: SerializableUUID
    name: str
    description: str | None = None
    public: bool = False
    public_grades: bool = False
    author: SerializableUUID

    @staticmethod
    def from_skill_tree_entity(entity: SkillTreeEntity) -> "SkillTreeEntityResponse":
        return SkillTreeEntityResponse(
            uid=entity.uid,
            name=entity.info.name,
            description=entity.info.description,
            public=entity.info.public,
            public_grades=entity.info.public_grades,
            author=entity.info.author,
        )


class SkillTreeFilter(BaseModel):
    author: UUID | None = None
    name: str | None = None
    public: bool | None = None

    @staticmethod
    def from_query(
        author: Annotated[UUID | None, Query()] = None,
        name: Annotated[str | None, Query()] = None,
        public: Annotated[bool | None, Query()] = None,
    ) -> "SkillTreeFilter":
        return SkillTreeFilter(
            author=author,
            name=name,
            public=public,
        )


class PutSkillTreeRequest(BaseModel):
    name: str
    description: str | None

    def to_skill_tree_info_update(self) -> SkillTreeInfoUpdate:
        return SkillTreeInfoUpdate(**self.model_dump())


PutSkillTreeRequestBody = Annotated[PutSkillTreeRequest, Body()]
SkillTreeFilterQuery = Annotated[SkillTreeFilter, Depends(SkillTreeFilter.from_query)]
PostSkillTreeRequestBody = Annotated[PostSkillTreeRequest, Body()]
