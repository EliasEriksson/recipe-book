from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from .. import models
from api import schemas


class Recipes:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> Sequence[models.Recipe]:
        query = select(models.Recipe)
        async with self._session.begin():
            result = await self._session.execute(query)
        return result.scalars().all()

    async def fetch_by_id(
        self, id: UUID
    ) -> tuple[models.Recipe, models.RecipeTranslation] | None:
        recipe_query = select(models.Recipe).where(models.Recipe.id == id)
        translation_query = select(models.RecipeTranslation).where(
            models.RecipeTranslation.recipe_id == id
        )
        async with self._session.begin():
            recipe = (await self._session.execute(recipe_query)).scalars().one_or_none()
            translation = (
                (await self._session.execute(translation_query)).scalars().one_or_none()
            )
        return (recipe, translation) if recipe and translation else None

    async def create(
        self, creatable: schemas.recipe.CreateProtocol
    ) -> tuple[models.Recipe, models.RecipeTranslation]:
        async with self._session.begin():
            recipe = models.Recipe.create(creatable)
            self._session.add(recipe)
            await self._session.flush()
            translation = models.RecipeTranslation.create(recipe, creatable)
            self._session.add(translation)
        return recipe, translation

    async def update(self, recipe: schemas.recipe.RecipeProtocol) -> models.Recipe:
        pass

    async def delete_by_id(self, id: UUID) -> bool:
        query = delete(models.Recipe).where(models.Recipe.id == id)
        async with self._session.begin():
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0
