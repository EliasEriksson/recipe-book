from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from .. import models
from api import schemas
from .paging import Page
from .paging import PageResult
from datetime import datetime


class Result:
    language: models.Language

    def __init__(self, language: models.Language) -> None:
        self.language = language

    @property
    def modified(self) -> datetime:
        return self.language.modified


class Languages(Page):
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[Result]:
        query = select(models.Language)
        query = self.page(query, limit, offset)
        async with self._session.begin():
            results = (await self._session.execute(query)).scalars().all()
        return PageResult(
            limit,
            offset,
            [Result(result) for result in results],
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
        query = self.page(query, limit, offset)
        async with self._session.begin():
            results = (await self._session.execute(query)).scalars().all()
        return PageResult(
            limit,
            offset,
            [Result(language) for language in results],
        )

    async def fetch_by_id(self, id: UUID) -> Result | None:
        query = select(models.Language).where(models.Language.id == id)
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().one_or_none()
        return Result(result) if result else None

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
        async with self._session.begin():
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0
