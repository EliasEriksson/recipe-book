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
            else self.translation.modified
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

    async def fetch_best_translation(
        self, id: UUID, languages: List[models.Language]
    ) -> TranslationResult | None:
        async with self._session.begin():
            for language in languages:
                query = (
                    select(models.RecipeTranslation)
                    .where(models.RecipeTranslation.recipe_id == id)
                    .where(models.RecipeTranslation.language_id == language.id)
                )
                result = (await self._session.execute(query)).scalars().one_or_none()
                if not result:
                    continue
                return TranslationResult(result)
        return None

    async def list(self, language_codes: List[str]) -> List[Result]:
        query = select(models.Recipe)
        languages = await self._languages.fetch_by_codes(language_codes)
        # async with self._session.begin():

        return []
        # query = select(models.Recipe)
        # async with self._session.begin():
        #     results = (await self._session.execute(query)).scalars().all()
        # return ListResult([Result(result, ) for result in results])

    async def fetch_by_id(
        self, id: UUID, languages_codes: List[str] | None = None
    ) -> Result | None:
        query = select(models.Recipe).where(models.Recipe.id == id)
        languages = await self._languages.fetch_by_codes(languages_codes)
        async with self._session.begin():
            recipe = (await self._session.execute(query)).scalars().one_or_none()
            if not recipe:
                return None
        translation_result = await self.fetch_best_translation(
            id, [result.language for result in languages]
        )
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
