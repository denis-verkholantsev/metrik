from dataclasses import dataclass
from uuid import UUID

import edgedb

from app.core.tree.models import (
    SkillTreeEntity,
    SkillTreeInfo,
    SkillTreeInfoUpdate,
    SkillTreeQuery,
)
from app.core.tree.services import SkillTreeRepository
from scripts import (
    add_like_in_skill_tree,
    insert_tree,
    remove_like_in_skill_tree,
    select_many_tree_filter_author,
    select_many_tree_filter_author_name,
    select_tree_filter_uid,
    update_tree_info,
)


@dataclass(slots=True)
class EdgeDBSkillTreeRepository(SkillTreeRepository):
    executor: edgedb.AsyncIOExecutor

    async def insert_one(self, info: SkillTreeInfo) -> SkillTreeEntity:
        result = await insert_tree(
            self.executor,
            name=info.name,
            description=info.description,
            public=info.public,
            public_grades=info.public_grades,
            author=info.author,
        )

        return SkillTreeEntity(uid=result.id, info=info)

    async def select_many(
        self,
        query: SkillTreeQuery,
        page: int = 0,
        per_page: int = 10,
    ) -> list[SkillTreeEntity]:
        if query.name:
            result = await select_many_tree_filter_author_name(
                self.executor,
                author=query.author,
                public=query.public,
                name=f"%{query.name}%",
                offset=page * per_page,
                limit=per_page,
            )
        else:
            result = await select_many_tree_filter_author(
                self.executor,
                author=query.author,
                public=query.public,
                offset=page * per_page,
                limit=per_page,
            )

        return [
            SkillTreeEntity(
                uid=r.id,
                info=SkillTreeInfo(
                    name=r.name,
                    description=r.description,
                    public=r.public,
                    public_grades=r.public_grades,
                    author=query.author,
                ),
            )
            for r in result
        ]

    async def update_one_info(
        self,
        tree_uid: UUID,
        author: UUID,
        update: SkillTreeInfoUpdate,
    ) -> UUID | None:
        result = await update_tree_info(
            self.executor,
            uid=tree_uid,
            author=author,
            name=update.name,
            description=update.description,
        )

        if not result:
            return None

        return result.id

    async def select_one(self, uid: UUID) -> SkillTreeEntity | None:
        result = await select_tree_filter_uid(self.executor, uid=uid)

        if not result:
            return None

        return SkillTreeEntity(
            uid=result.id,
            info=SkillTreeInfo(
                name=result.name,
                description=result.description,
                public=result.public,
                public_grades=result.public_grades,
                author=result.author.id,
            ),
        )

    async def add_like(self, tree_uid: UUID, user_uid: UUID) -> bool:
        result = await add_like_in_skill_tree(
            self.executor, tree_uid=tree_uid, user_uid=user_uid
        )

        return result is not None

    async def remove_like(self, tree_uid: UUID, user_uid: UUID) -> bool:
        result = await remove_like_in_skill_tree(
            self.executor, tree_uid=tree_uid, user_uid=user_uid
        )
        return result is not None
