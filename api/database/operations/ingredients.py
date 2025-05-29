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


class Result:
    ingredient: models.Ingredient
    translation: models.IngredientTranslation

    def __init__(
        self, ingredient: models.Ingredient, translation: models.IngredientTranslation
    ) -> None:
        self.ingredient = ingredient
        self.translation = translation

    @property
    def modified(self) -> datetime:
        return (
            self.ingredient.modified
            if self.ingredient.modified > self.translation.modified
            else self.translation.modified
        )


# noinspection DuplicatedCode
class Ingredients:
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
                models.IngredientTranslation,
                select(
                    models.IngredientTranslation,
                    func.min(models.IngredientTranslation.created),
                )
                .distinct(models.IngredientTranslation.ingredient_id)
                .group_by(
                    models.IngredientTranslation.ingredient_id,
                    models.IngredientTranslation.language_id,
                )
                .subquery("translation"),
                flat=True,
            )
            query = (
                select(translation, models.Ingredient)
                .order_by(desc(cast(ColumnElement, translation.created)))
                .options(selectinload(cast(QueryableAttribute, translation.ingredient)))
            )
        else:
            query = (
                select(models.IngredientTranslation)
                .join(models.Language)
                .where(models.Language.code == language_code)
                .order_by(desc(models.IngredientTranslation.created))
                .options(selectinload(models.IngredientTranslation.ingredient))
            )
        query = query.join(models.Ingredient)
        return await self._operator.list(
            query, lambda result: Result(result.ingredient, result), limit, offset
        )

    async def fetch_by_id(self, id: UUID, language_id: UUID) -> Result:
        query = (
            select(models.IngredientTranslation)
            .where(models.IngredientTranslation.ingredient_id == id)
            .where(models.IngredientTranslation.language_id == language_id)
            .join(models.Ingredient)
            .options(selectinload(models.IngredientTranslation.ingredient))
        )
        return await self._operator.fetch(
            query, lambda result: Result(result.ingredient, result)
        )

    async def create(self, data: schemas.ingredient.CreateProtocol) -> Result:
        async with self._session.begin():
            ingredient = models.Ingredient.create(data)
            self._session.add(ingredient)
            await self._session.flush()
            translation = models.IngredientTranslation.create(ingredient, data)
            self._session.add(translation)
        return Result(ingredient, translation)

    async def update(
        self, id: UUID, data: schemas.ingredient.IngredientProtocol
    ) -> Result:
        query = (
            select(models.Ingredient)
            .join(models.IngredientTranslation)
            .where(models.Ingredient.id == id)
            .options(selectinload(models.Ingredient.translations))
        )
        async with self._session.begin():
            ingredient = await self._operator.execute_scalars_first(
                self._session, query
            )
            for translation in ingredient.translations:
                if translation.language_id == data.language_id:
                    translation.update(data)
                    break
            else:
                translation = models.IngredientTranslation.create(ingredient, data)
                self._session.add(translation)
                ingredient.translations.append(translation)
            ingredient.update(data)
        return Result(ingredient, translation)

    async def delete(self, id: UUID) -> bool:
        query = delete(models.Ingredient).where(models.Ingredient.id == id)
        return await self._operator.delete(query)

    async def delete_translation(self, id: UUID, language_id: UUID) -> bool:
        query = (
            delete(models.IngredientTranslation)
            .where(models.IngredientTranslation.language_id == language_id)
            .where(
                models.IngredientTranslation.ingredient_id
                == select(models.IngredientTranslation.ingredient_id)
                .where(models.IngredientTranslation.ingredient_id == id)
                .group_by(models.IngredientTranslation.ingredient_id)
                .having(func.count("*") > 1)
                .scalar_subquery()
            )
        )
        return await self._operator.delete(query)
