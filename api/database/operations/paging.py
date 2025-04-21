from typing import *
from sqlalchemy import Select


class PageResult[T]:
    limit: int | None
    offset: int | None
    results: List[T]

    def __init__(
        self,
        limit: int | None,
        offset: int | None,
        count: int,
        results: List[T],
    ) -> None:
        self.limit = limit
        self.offset = offset
        self.count = count
        self.results = results


class Page:
    @staticmethod
    def page[T](
        query: Select[T],
        limit: int | None = None,
        offset: int | None = None,
    ) -> Select[T]:
        if limit is not None:
            query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
        return query
