from datetime import datetime
from typing import *
from uuid import UUID

from sqlalchemy import ColumnElement, and_, delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import QueryableAttribute, aliased, contains_eager

from api import schemas
from api.database.result import PageResult, TranslatedResult

from .. import models
from ..operator import Operator
from .recipes import Recipes


class Result(
    TranslatedResult[models.RecipeIngredient, models.RecipeIngredientTranslation]
): ...


class RecipeIngredients:
    _session: AsyncSession
    _operator: Operator
    _recipes: Recipes

    def __init__(self, session: AsyncSession, recipes: Recipes) -> None:
        self._session = session
        self._operator = Operator(session)
        self._recipes = recipes

    async def list(
        self,
        recipe_id: UUID,
        language_code: str | None,
        limit: int | None = None,
        offset: int | None = None,
        *,
        ingredient_id: UUID | None = None,
    ) -> PageResult[Result]:
        query = select(models.RecipeIngredientTranslation)
        if language_code is None:
            recipe_translation = self._recipes.original_translation_subquery(recipe_id)
            query = query.where(
                models.RecipeIngredientTranslation.language_id
                == recipe_translation.language_id
            )
        else:
            query = (
                select(models.RecipeIngredientTranslation)
                .join(
                    models.Language,
                    onclause=(
                        models.Language.id
                        == models.RecipeIngredientTranslation.language_id
                    ),
                )
                .where(models.Language.code == language_code)
            )
        query = (
            query.join(
                models.RecipeIngredient,
                onclause=and_(
                    models.RecipeIngredient.recipe_id
                    == models.RecipeIngredientTranslation.recipe_id,
                    models.RecipeIngredient.ingredient_id
                    == models.RecipeIngredientTranslation.ingredient_id,
                ),
            )
            .order_by(desc(models.RecipeIngredientTranslation.created))
            .options(
                contains_eager(models.RecipeIngredientTranslation.recipe_ingredient)
            )
        )
        query = query.where(models.RecipeIngredient.recipe_id == recipe_id)
        if ingredient_id is not None:
            query = query.where(models.RecipeIngredient.ingredient_id == ingredient_id)
        return await self._operator.list(
            query,
            lambda result: Result(result.recipe_ingredient, result),
            limit,
            offset,
        )

    async def create(self, data: schemas.recipe_ingredient.CreateProtocol) -> Result:
        async with self._session.begin():
            recipe_ingredient = models.RecipeIngredient.create(data)
            self._session.add(recipe_ingredient)
            await self._session.flush()
            translation = models.RecipeIngredientTranslation.create(
                recipe_ingredient, data
            )
            self._session.add(translation)
        return Result(recipe_ingredient, translation)
