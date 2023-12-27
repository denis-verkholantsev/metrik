from uuid import UUID

from pydantic import BaseModel


class Coordinates(BaseModel):
    x: float
    y: float


class SkillInfo(BaseModel):
    name: str
    description: str | None = None
    tree: UUID
    author: UUID
    position: Coordinates


class SkillInfoUpdate(BaseModel):
    name: str
    description: str | None = None
    position: Coordinates


class SkillEntity(BaseModel):
    uid: UUID
    info: SkillInfo


class GradeInfo(BaseModel):
    value: int
    public: bool = False
    skill: UUID
    author: UUID


class GradeEntity(BaseModel):
    uid: UUID
    info: GradeInfo


class KnowledgeInfo(BaseModel):
    name: str
    content: str
    skill: UUID
    author: UUID


class KnowledgeEntity(BaseModel):
    uid: UUID
    info: KnowledgeInfo


class KnowledgeInfoUpdate(BaseModel):
    name: str
    content: str


class SkillTreeInfo(BaseModel):
    name: str
    public: bool = False
    public_grades: bool = False
    description: str | None = None
    author: UUID


class SkillTreeEntity(BaseModel):
    uid: UUID
    info: SkillTreeInfo


class SkillTreeQuery(BaseModel):
    author: UUID
    public: bool | None = None
    name: str | None = None


class SkillTreeInfoUpdate(BaseModel):
    name: str
    description: str | None


class SkillLinkInfo(BaseModel):
    source: UUID
    target: UUID
    tree: UUID
