from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api import schemas
from api.database.page_result import PageResult

from .. import models
from ..operator import Operator


class Result:
    language: models.Language

    def __init__(self, language: models.Language) -> None:
        self.language = language

    @property
    def modified(self) -> datetime:
        return self.language.modified


class Languages:
    _operator: Operator
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._operator = Operator(session)

    async def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[Result]:
        query = select(models.Language)
        return await self._operator.list(
            query, lambda result: Result(result), limit, offset
        )

    async def list_by_recipe(
        self,
        recipe_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[Result]:
        query = (
            select(models.Language)
            .join(models.RecipeTranslation)
            .join(models.Recipe)
            .where(models.Recipe.id == recipe_id)
        )
        return await self._operator.list(
            query, lambda result: Result(result), limit, offset
        )

    async def fetch_by_id(self, id: UUID) -> Result:
        query = select(models.Language).where(models.Language.id == id)
        return await self._operator.fetch(query, lambda result: Result(result))

    async def create(self, language: schemas.language.CreateProtocol) -> Result:
        result = models.Language.create(language)
        async with self._session.begin():
            self._session.add(result)
        return Result(result)

    async def update(
        self, id: UUID, language: schemas.language.LanguageProtocol
    ) -> Result:
        result = await self.fetch_by_id(id)
        async with self._session.begin():
            result.language.update(language)
        return Result(result.language)

    async def delete(self, id: UUID) -> bool:
        query = delete(models.Language).where(models.Language.id == id)
        return await self._operator.delete(query)
