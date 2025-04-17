from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from .. import models
from api import schemas
from .languages import Languages


class Result:
    recipe: models.Recipe
    translation: models.RecipeTranslation

    def __init__(
        self, recipe: models.Recipe, translation: models.RecipeTranslation
    ) -> None:
        self.recipe = recipe
        self.translation = translation

    @property
    def last_modified(self) -> str:
        return (
            self.recipe.last_modified
            if self.recipe.modified > self.translation.modified
            else self.translation.last_modified
        )


class TranslationResult:
    translation: models.RecipeTranslation

    def __init__(self, translation: models.RecipeTranslation) -> None:
        self.translation = translation


class Recipes:
    _session: AsyncSession
    _languages: Languages

    def __init__(self, session: AsyncSession, languages: Languages) -> None:
        self._session = session
        self._languages = languages

    async def fetch_translation(
        self, id: UUID, language: models.Language
    ) -> TranslationResult | None:
        query = (
            select(models.RecipeTranslation)
            .where(models.RecipeTranslation.recipe_id == id)
            .where(models.RecipeTranslation.language_id == language.id)
        )
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().one_or_none()
        if result:
            return TranslationResult(result)
        query = (
            select(models.RecipeTranslation)
            .where(models.RecipeTranslation.recipe_id == id)
            .order_by(models.RecipeTranslation.created)
        )
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().one_or_none()
        if result:
            return TranslationResult(result)
        return None

    async def list(self, language_codes: List[str]) -> List[Result]:
        query = select(models.Recipe)
        languages = await self._languages.fetch_by_codes(language_codes)
        return []

    async def fetch_by_id(self, id: UUID, language_code: str) -> Result | None:
        query = select(models.Recipe).where(models.Recipe.id == id)
        language_result = await self._languages.fetch_by_code(language_code)
        if not language_result:
            return None
        async with self._session.begin():
            recipe = (await self._session.execute(query)).scalars().one_or_none()
            if not recipe:
                return None
        translation_result = await self.fetch_translation(id, language_result.language)
        if not translation_result:
            return None
        return Result(recipe, translation_result.translation)

    async def create(self, creatable: schemas.recipe.CreateProtocol) -> Result:
        async with self._session.begin():
            recipe = models.Recipe.create(creatable)
            self._session.add(recipe)
            await self._session.flush()
            translation = models.RecipeTranslation.create(recipe, creatable)
            self._session.add(translation)
        return Result(recipe, translation)

    async def update(self, recipe: schemas.recipe.RecipeProtocol) -> Result:
        pass

    async def delete_by_id(self, id: UUID) -> bool:
        query = delete(models.Recipe).where(models.Recipe.id == id)
        async with self._session.begin():
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0
