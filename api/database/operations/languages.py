from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from .. import models
from api import schemas


class Result:
    language: models.Language

    def __init__(self, language: models.Language) -> None:
        self.language = language

    @property
    def last_modified(self) -> str:
        return self.language.last_modified


class Languages:
    _session: AsyncSession
    model: Type[models.Language]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[Result]:
        query = select(models.Language)
        async with self._session.begin():
            results = (await self._session.execute(query)).scalars().all()
        return [Result(result) for result in results]

    async def list_by_recipe(self, recipe_id: UUID) -> List[Result]:
        query = (
            select(models.Language)
            .join(models.RecipeTranslation)
            .join(models.Recipe)
            .where(models.Recipe.id == recipe_id)
        )
        async with self._session.begin():
            results = (await self._session.execute(query)).scalars().all()
        return [Result(language) for language in results]

    async def fetch_by_id(self, id: UUID) -> Result | None:
        query = select(models.Language).where(models.Language.id == id)
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().one_or_none()
        return Result(result) if result else None

    async def fetch_by_code(self, code: str) -> Result | None:
        query = select(models.Language).where(models.Language.code == code)
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().one_or_none()
        return Result(result) if result else None

    async def fetch_by_codes(self, codes: List[str]) -> List[Result]:
        fetched_codes = set()
        results: list[models.Language] = []
        for code in codes:
            if code in fetched_codes:
                continue
            fetched_codes.add(code)
            if (result := await self.fetch_by_code(code)) is None:
                continue
            results.append(result.language)
        return [Result(result) for result in results]

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

    async def delete_by_id(self, id: UUID) -> bool:
        query = delete(models.Language).where(models.Language.id == id)
        async with self._session.begin():
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0
