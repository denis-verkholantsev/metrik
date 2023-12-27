from datetime import date, datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends, Query
from pydantic import BaseModel, PlainSerializer


def to_isoformat(dt: date | datetime) -> str:
    return dt.isoformat()


def to_str(obj: Any) -> str:
    return str(obj)


SerializableDate = Annotated[
    date,
    PlainSerializer(to_isoformat, return_type=str, when_used="always"),
]

SerializableUUID = Annotated[
    UUID, PlainSerializer(to_str, return_type=str, when_used="always")
]


# TODO add validation with Positive and NonNegativeInt
class Pagination(BaseModel):
    page: int
    per_page: int

    @staticmethod
    def from_query(
        page: Annotated[int, Query()] = 0,
        per_page: Annotated[int, Query()] = 10,
    ) -> "Pagination":
        return Pagination(page=page, per_page=per_page)


PaginationQuery = Annotated[Pagination, Depends(Pagination.from_query)]
