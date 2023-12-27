from dataclasses import dataclass
from uuid import UUID

import edgedb

from app.core.tree.errors import SkillTreeNotFoundError
from app.core.tree.models import SkillLinkInfo
from app.core.tree.services import SkillLinkRepository
from scripts import delete_link, insert_link, select_many_link


@dataclass(slots=True)
class EdgeDBSkillLinkRepository(SkillLinkRepository):
    executor: edgedb.AsyncIOExecutor

    async def insert_one(self, info: SkillLinkInfo) -> None:
        result = await insert_link(
            self.executor,
            target=info.target,
            source=info.source,
            tree=info.tree,
        )

        if not result:
            raise SkillTreeNotFoundError()

    async def select_many(
        self,
        tree_uid: UUID,
        author_uid: UUID,
    ) -> list[SkillLinkInfo]:
        result = await select_many_link(
            self.executor,
            tree=tree_uid,
            author=author_uid,
        )

        return [
            SkillLinkInfo(source=source.id, target=target.id, tree=tree_uid)
            for source in result
            for target in source.contains
        ]

    async def delete_one(self, info: SkillLinkInfo, author: UUID) -> None:
        await delete_link(
            self.executor,
            tree=info.tree,
            source=info.source,
            target=info.target,
            author=author,
        )
