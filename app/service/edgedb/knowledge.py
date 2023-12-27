from dataclasses import dataclass
from typing import Any
from uuid import UUID

import edgedb

from app.core.tree.models import KnowledgeEntity, KnowledgeInfo, KnowledgeInfoUpdate
from app.core.tree.services import KnowledgeRepository
from scripts import (
    delete_knowledge,
    insert_knowledge,
    select_many_knowledge,
    update_knowledge_info,
)


@dataclass(slots=True)
class EdgeDBKnowledgeRepository(KnowledgeRepository):
    executor: edgedb.AsyncIOExecutor

    async def insert_one(self, info: KnowledgeInfo) -> KnowledgeEntity | None:
        result = await insert_knowledge(
            self.executor,
            name=info.name,
            content=info.content,
            user_uid=info.author,
            skill_uid=info.skill,
        )

        if not result:
            return None

        return KnowledgeEntity(uid=result.id, info=info)

    async def select_many(
        self, skill_uid: UUID, user_uid: UUID
    ) -> list[KnowledgeEntity]:
        result: list[Any] = await select_many_knowledge(
            self.executor,
            skill_uid=skill_uid,
            user_uid=user_uid,
        )

        return [
            KnowledgeEntity(
                uid=item.id,
                info=KnowledgeInfo(
                    name=item.name,
                    content=item.content,
                    skill=item.skill.id,
                    author=item.author.id,
                ),
            )
            for item in result
        ]

    async def update_one_info(
        self, knowledge_uid: UUID, author_uid: UUID, update: KnowledgeInfoUpdate
    ) -> UUID | None:
        result = await update_knowledge_info(
            self.executor,
            knowledge_uid=knowledge_uid,
            author_uid=author_uid,
            name=update.name,
            content=update.content,
        )

        if not result:
            return None

        return result.id

    async def delete_one(self, knowledge_uid: UUID, author_uid: UUID) -> None:
        await delete_knowledge(
            self.executor, knowledge_uid=knowledge_uid, author_uid=author_uid
        )
