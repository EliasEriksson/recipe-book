from typing import *

from sqlalchemy import Delete, Select, func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.roles import FromClauseRole

from .page_result import PageResult


class Operator:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list[T, TResult](
        self,
        query: Select[T],
        transformer: Callable[[T], TResult],
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[TResult]:
        async with self._session.begin():
            results = await self._session.execute(self.page(query, limit, offset))
            count = await self._session.execute(self.count(query))
        return PageResult(
            limit,
            offset,
            count.scalars().one(),
            [transformer(result) for result in results.scalars().all()],
        )

    async def fetch[T, TResult](
        self,
        query: Select[T],
        transformer: Callable[[T], TResult],
    ) -> TResult:
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().first()
        if result is None:
            raise NoResultFound("No row was found when one was required")
        return transformer(result)

    async def delete[T](self, query: Delete[T]) -> bool:
        async with self._session.begin():
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0

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

    @staticmethod
    def count[T](query: Select[T]) -> Select[Tuple[int]]:
        return select(func.count("*")).select_from(cast(FromClauseRole, query))
