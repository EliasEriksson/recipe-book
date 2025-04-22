from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from .. import models
from api import schemas
from api.database.page import Page
from api.database.page import PageResult
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
        async with self._session.begin():
            results = (
                (await self._session.execute(self.page(query, limit, offset)))
                .scalars()
                .all()
            )
            count = (await self._session.execute(self.count(query))).scalars().one()
        return PageResult(
            limit,
            offset,
            count,
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
        async with self._session.begin():
            results = (
                (await self._session.execute(self.page(query, limit, offset)))
                .scalars()
                .all()
            )
            count = (await self._session.execute(self.count(query))).scalars().one()
        return PageResult(
            limit,
            offset,
            count,
            [Result(language) for language in results],
        )

    async def fetch_by_id(self, id: UUID) -> Result:
        query = select(models.Language).where(models.Language.id == id)
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().one()
        return Result(result)

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
