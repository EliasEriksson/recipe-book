from __future__ import annotations

from typing import *
from uuid import UUID

from sqlalchemy import Double, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api import schemas

from ..constants import CASCADE, Cascades
from .base import Base

if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .recipe import Recipe
    from .recipe_ingredient_translation import RecipeIngredientTranslation
    from .unit import Unit


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"
    recipe_id: Mapped[UUID] = mapped_column(
        ForeignKey("recipe.id", ondelete=CASCADE),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    ingredient_id: Mapped[UUID] = mapped_column(
        ForeignKey("ingredient.id", ondelete=CASCADE),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    unit_id: Mapped[UUID] = mapped_column(
        ForeignKey("unit.id", ondelete=CASCADE),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(
        Double(),
        nullable=False,
    )
    recipe: Mapped[Recipe] = relationship(
        back_populates="recipe_ingredients",
    )
    ingredient: Mapped[Ingredient] = relationship(
        back_populates="recipe_ingredients",
    )
    unit: Mapped[Unit] = relationship(
        back_populates="recipe_ingredients",
    )
    translations: Mapped[List[RecipeIngredientTranslation]] = relationship(
        back_populates="recipe_ingredient",
        foreign_keys="[RecipeIngredientTranslation.recipe_id, RecipeIngredientTranslation.ingredient_id]",
        cascade=Cascades.default(),
    )

    @classmethod
    def create(cls, schema: schemas.RecipeIngredient) -> Self:
        return cls(
            recipe_id=schema.recipe_id,
            ingredient_id=schema.ingredient_id,
            unit_id=schema.unit_id,
            amount=schema.amount,
        )

    def update(
        self, recipe: schemas.recipe_ingredient.RecipeIngredientProtocol
    ) -> Self:
        self.recipe_id = recipe.recipe_id
        self.ingredient_id = recipe.ingredient_id
        self.unit_id = recipe.unit_id
        self.amount = recipe.amount
        return self
