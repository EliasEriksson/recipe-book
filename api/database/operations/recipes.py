from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.orm import selectinload
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
        self, id: UUID, language: models.Language, *, original_fallback=False
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
        if not original_fallback:
            return None
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

    async def list(self, language_code: str | None) -> List[Result]:
        query = select(models.RecipeTranslation, models.Recipe)
        query = query.join(models.Recipe).options(
            selectinload(models.RecipeTranslation.recipe)
        )
        async with self._session.begin():
            results = (await self._session.execute(query)).scalars().all()
        for result in results:
            print(result.recipe)
        # raise NotImplemented
        # query = select(models.Recipe).join(models.RecipeTranslation)
        # if language_code is not None:
        #     query = query.join(models.Language).where(
        #         models.Language.code == language_code
        #     )
        # else:
        #     query = query
        # language = await self._languages.fetch_by_code(language_code)
        # language_result = await self._languages.fetch_by_code(language_code)
        # if not language_result:
        #     return []
        # async with self._session.begin():
        #     recipes = (await self._session.execute(query)).scalars().all()
        # results = [
        #     Result(recipe, translation_result.translation)
        #     for recipe in recipes
        #     if (
        #         translation_result := await self.fetch_translation(
        #             recipe.id, language_result.language
        #         )
        #     )
        # ]
        # return results
        return []

    async def fetch_by_id(
        self, id: UUID, language_code: str | None = None
    ) -> Result | None:
        query = select(models.Recipe).where(models.Recipe.id == id)
        language_result = await self._languages.fetch_by_code(language_code)
        if not language_result:
            return None
        async with self._session.begin():
            recipe = (await self._session.execute(query)).scalars().one_or_none()
            if not recipe:
                return None
        translation_result = await self.fetch_translation(
            id, language_result.language, original_fallback=True
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

    async def update(self, id: UUID, recipe: schemas.recipe.RecipeProtocol) -> Result:
        query = (
            select(models.Recipe, models.RecipeTranslation)
            .join(models.RecipeTranslation)
            .where(models.Recipe.id == id)
            .options(selectinload(models.Recipe.translations))
        )
        async with self._session.begin():
            result = (await self._session.execute(query)).scalars().one()
            for translation in result.translations:
                if translation.language_id == recipe.language_id:
                    translation.update(recipe)
                    break
            else:
                translation = models.RecipeTranslation.create(result, recipe)
                self._session.add(translation)
                result.translations.append(translation)
            result.update(recipe)
        return Result(result, translation)

    async def delete_by_id(self, id: UUID) -> bool:
        query = delete(models.Recipe).where(models.Recipe.id == id)
        async with self._session.begin():
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0
