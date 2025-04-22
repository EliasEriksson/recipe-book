from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, desc, func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api import schemas
from api.database.page_result import PageResult

from .. import models
from ..operator import Operator
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
    def modified(self) -> datetime:
        return (
            self.recipe.modified
            if self.recipe.modified > self.translation.modified
            else self.translation.modified
        )


class Recipes:
    _session: AsyncSession
    _languages: Languages
    _operator: Operator

    def __init__(self, session: AsyncSession, languages: Languages) -> None:
        self._session = session
        self._operator = Operator(session)
        self._languages = languages

    async def list(
        self,
        language_code: str | None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[Result]:
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
            )
        else:
            query = (
                select(models.RecipeTranslation)
                .join(models.Language)
                .where(models.Language.code == language_code)
                .order_by(desc(models.RecipeTranslation.created))
            )
        query = query.join(models.Recipe).options(
            selectinload(models.RecipeTranslation.recipe)
        )
        return await self._operator.list(
            query,
            lambda result: Result(result.recipe, result),
            limit,
            offset,
        )

    async def fetch_by_id(self, id: UUID, language_id: UUID) -> Result:
        query = (
            select(models.RecipeTranslation)
            .where(models.RecipeTranslation.language_id == language_id)
            .where(models.RecipeTranslation.recipe_id == id)
            .join(models.Recipe)
            .options(selectinload(models.RecipeTranslation.recipe))
        )
        return await self._operator.fetch(
            query, lambda result: Result(result.recipe, result)
        )

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
            select(models.Recipe)
            .join(models.RecipeTranslation)
            .where(models.Recipe.id == id)
            .options(selectinload(models.Recipe.translations))
        )
        async with self._session.begin():
            recipe = (await self._session.execute(query)).scalars().first()
            if recipe is None:
                raise NoResultFound("No row was found when one was required")
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

    async def delete(self, id: UUID) -> bool:
        query = delete(models.Recipe).where(models.Recipe.id == id)
        return await self._operator.delete(query)

    async def delete_translation(self, id: UUID, language_id: UUID) -> bool:
        query = (
            delete(models.RecipeTranslation)
            .where(models.RecipeTranslation.recipe_id == id)
            .where(models.RecipeTranslation.language_id == language_id)
        )
        return await self._operator.delete(query)
