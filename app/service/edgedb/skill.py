from dataclasses import dataclass
from uuid import UUID

import edgedb

from app.core.tree.models import Coordinates, SkillEntity, SkillInfo, SkillInfoUpdate
from app.core.tree.services import SkillRepository
from scripts import (
    delete_skill,
    insert_skill,
    select_many_skill_filter_tree,
    select_skill,
    update_skill_info,
)


@dataclass(slots=True)
class EdgeDBSkillRepository(SkillRepository):
    executor: edgedb.AsyncIOExecutor

    async def insert_one(self, info: SkillInfo) -> SkillEntity | None:
        result = await insert_skill(
            self.executor,
            name=info.name,
            description=info.description,
            author=info.author,
            tree=info.tree,
            x=info.position.x,
            y=info.position.y,
        )

        if not result:
            return None

        return SkillEntity(uid=result.id, info=info)

    async def select_many(
        self, tree_uid: UUID, user_uid: UUID
    ) -> list[SkillEntity] | None:
        result = await select_many_skill_filter_tree(
            self.executor,
            tree=tree_uid,
            user=user_uid,
        )
        return [
            SkillEntity(
                uid=r.id,
                info=SkillInfo(
                    name=r.name,
                    description=r.description,
                    tree=tree_uid,
                    author=r.author.id,
                    position=Coordinates(x=r.x, y=r.y),
                ),
            )
            for r in result
        ]

    async def update_one_info(
        self, skill_uid: UUID, author: UUID, update: SkillInfoUpdate
    ) -> UUID | None:
        result = await update_skill_info(
            self.executor,
            skill=skill_uid,
            author=author,
            name=update.name,
            description=update.description,
            x=update.position.x,
            y=update.position.y,
        )

        if not result:
            return None

        return result.id

    async def select_one(self, skill_uid: UUID, author_uid: UUID) -> SkillEntity | None:
        result = await select_skill(
            self.executor, skill_uid=skill_uid, author_uid=author_uid
        )

        if result is None:
            return None

        return SkillEntity(
            uid=result.id,
            info=SkillInfo(
                name=result.name,
                description=result.description,
                tree=result.tree.id,
                author=author_uid,
                position=Coordinates(x=result.x, y=result.y),
            ),
        )

    async def delete_one(self, skill_uid: UUID, author_uid: UUID) -> None:
        await delete_skill(self.executor, skill_uid=skill_uid, author_uid=author_uid)
