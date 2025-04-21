from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import func
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
        if language_code is None:
            query = (
                select(
                    models.RecipeTranslation, func.min(models.RecipeTranslation.created)
                )
                .distinct(models.RecipeTranslation.recipe_id)
                .group_by(
                    models.RecipeTranslation.recipe_id,
                    models.RecipeTranslation.language_id,
                )
                .join(models.Recipe)
                .options(selectinload(models.RecipeTranslation.recipe))
            )
        else:
            query = (
                select(models.RecipeTranslation)
                .join(models.Language)
                .where(models.Language.code == language_code)
                .join(models.Recipe)
                .options(selectinload(models.RecipeTranslation.recipe))
            )
        async with self._session.begin():
            translations = (await self._session.execute(query)).scalars().all()

        return [Result(translation.recipe, translation) for translation in translations]

    async def fetch_by_id(self, id: UUID, language_id: UUID) -> Result | None:
        query = (
            select(models.RecipeTranslation)
            .where(models.RecipeTranslation.language_id == language_id)
            .where(models.RecipeTranslation.recipe_id == id)
            .join(models.Recipe)
            .options(selectinload(models.RecipeTranslation.recipe))
        )
        async with self._session.begin():
            translation = (await self._session.execute(query)).scalars().one()
        return Result(translation.recipe, translation)

    async def create(self, creatable: schemas.recipe.CreateProtocol) -> Result:
        async with self._session.begin():
            recipe = models.Recipe.create(creatable)
            self._session.add(recipe)
            await self._session.flush()
            translation = models.RecipeTranslation.create(recipe, creatable)
            self._session.add(translation)
        return Result(recipe, translation)

    async def update(self, id: UUID, data: schemas.recipe.RecipeProtocol) -> Result:
        query = (
            select(models.Recipe, models.RecipeTranslation)
            .join(models.RecipeTranslation)
            .where(models.Recipe.id == id)
            .options(selectinload(models.Recipe.translations))
        )
        async with self._session.begin():
            recipe = (await self._session.execute(query)).scalars().one()
            for translation in recipe.translations:
                if translation.language_id == data.language_id:
                    translation.update(data)
                    break
            else:
                translation = models.RecipeTranslation.create(recipe, data)
                self._session.add(translation)
                recipe.translations.append(translation)
            recipe.update(data)
        return Result(recipe, translation)

    async def delete_by_id(self, id: UUID) -> bool:
        query = delete(models.Recipe).where(models.Recipe.id == id)
        async with self._session.begin():
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0
