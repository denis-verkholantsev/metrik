from typing import Protocol
from uuid import UUID

from app.core.tree.models import (
    KnowledgeEntity,
    KnowledgeInfo,
    KnowledgeInfoUpdate,
    SkillEntity,
    SkillInfo,
    SkillInfoUpdate,
    SkillLinkInfo,
    SkillTreeEntity,
    SkillTreeInfo,
    SkillTreeInfoUpdate,
    SkillTreeQuery,
)


class SkillTreeRepository(Protocol):
    async def insert_one(self, info: SkillTreeInfo) -> SkillTreeEntity:
        raise NotImplementedError()

    async def select_many(
        self,
        query: SkillTreeQuery,
        page: int = 0,
        per_page: int = 10,
    ) -> list[SkillTreeEntity]:
        raise NotImplementedError()

    async def update_one_info(
        self,
        tree_uid: UUID,
        author: UUID,
        update: SkillTreeInfoUpdate,
    ) -> UUID | None:
        raise NotImplementedError()

    async def select_one(self, uid: UUID) -> SkillTreeEntity | None:
        raise NotImplementedError()

    async def add_like(self, tree_uid: UUID, user_uid: UUID) -> bool:
        raise NotImplementedError()

    async def remove_like(self, tree_uid: UUID, user_uid: UUID) -> bool:
        raise NotImplementedError()


class SkillRepository(Protocol):
    async def insert_one(self, info: SkillInfo) -> SkillEntity | None:
        raise NotImplementedError()

    async def select_many(
        self, tree_uid: UUID, user_uid: UUID
    ) -> list[SkillEntity] | None:
        raise NotImplementedError()

    async def select_one(self, skill_uid: UUID, author_uid: UUID) -> SkillEntity | None:
        raise NotImplementedError()

    async def update_one_info(
        self, skill_uid: UUID, author: UUID, update: SkillInfoUpdate
    ) -> UUID | None:
        raise NotImplementedError()

    async def delete_one(self, skill_uid: UUID, author_uid: UUID) -> SkillInfo | None:
        raise NotImplementedError()


class SkillLinkRepository(Protocol):
    async def insert_one(self, info: SkillLinkInfo) -> None:
        raise NotImplementedError()

    async def select_many(
        self,
        tree_uid: UUID,
        author_uid: UUID,
    ) -> list[SkillLinkInfo]:
        raise NotImplementedError()

    async def delete_one(self, info: SkillLinkInfo, author: UUID) -> None:
        raise NotImplementedError()


class KnowledgeRepository(Protocol):
    async def insert_one(self, info: KnowledgeInfo) -> KnowledgeEntity | None:
        raise NotImplementedError()

    async def select_many(
        self, skill_uid: UUID, user_uid: UUID
    ) -> list[KnowledgeEntity]:
        raise NotImplementedError()

    async def update_one_info(
        self, knowledge_uid: UUID, author_uid: UUID, update: KnowledgeInfoUpdate
    ) -> UUID | None:
        raise NotImplementedError()

    async def delete_one(self, knowledge_uid: UUID, author_uid: UUID) -> None:
        raise NotImplementedError()
