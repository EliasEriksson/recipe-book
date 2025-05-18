from datetime import datetime
from typing import *
from uuid import UUID

from sqlalchemy import ColumnElement, delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import QueryableAttribute, aliased, selectinload

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


# noinspection DuplicatedCode
class Recipes:
    _session: AsyncSession
    _operator: Operator

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._operator = Operator(session)

    async def list(
        self,
        language_code: str | None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[Result]:
        if language_code is None:
            translation = aliased(
                models.RecipeTranslation,
                select(
                    models.RecipeTranslation,
                    func.min(models.RecipeTranslation.created),
                )
                .distinct(models.RecipeTranslation.recipe_id)
                .group_by(
                    models.RecipeTranslation.recipe_id,
                    models.RecipeTranslation.language_id,
                )
                .subquery("translation"),
                flat=True,
            )
            query = (
                select(translation, models.Recipe)
                .order_by(desc(cast(ColumnElement, translation.created)))
                .options(selectinload(cast(QueryableAttribute, translation.recipe)))
            )
        else:
            query = (
                select(models.RecipeTranslation)
                .join(models.Language)
                .where(models.Language.code == language_code)
                .order_by(desc(models.RecipeTranslation.created))
                .options(selectinload(models.RecipeTranslation.recipe))
            )
        query = query.join(models.Recipe)
        return await self._operator.list(
            query,
            lambda result: Result(result.recipe, result),
            limit,
            offset,
        )

    async def fetch_by_id(self, id: UUID, language_id: UUID) -> Result:
        query = (
            select(models.RecipeTranslation)
            .where(models.RecipeTranslation.recipe_id == id)
            .where(models.RecipeTranslation.language_id == language_id)
            .join(models.Recipe)
            .options(selectinload(models.RecipeTranslation.recipe))
        )
        return await self._operator.fetch(
            query, lambda result: Result(result.recipe, result)
        )

    async def create(self, data: schemas.recipe.CreateProtocol) -> Result:
        async with self._session.begin():
            recipe = models.Recipe.create(data)
            self._session.add(recipe)
            await self._session.flush()
            translation = models.RecipeTranslation.create(recipe, data)
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
            recipe = await self._operator.execute_scalars_first(self._session, query)
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
