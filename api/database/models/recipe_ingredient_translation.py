from __future__ import annotations

from typing import *
from uuid import UUID

from sqlalchemy import ForeignKey, ForeignKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ... import schemas
from ..constants import CASCADE
from .base import Base

if TYPE_CHECKING:
    from .language import Language
    from .recipe_ingredient import RecipeIngredient


class RecipeIngredientTranslation(Base):
    __tablename__ = "recipe_ingredient_translation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["recipe_id", "ingredient_id"],
            ["recipe_ingredient.recipe_id", "recipe_ingredient.ingredient_id"],
            ondelete=CASCADE,
        ),
    )
    recipe_id: Mapped[UUID] = mapped_column(
        ForeignKey("recipe_ingredient.recipe_id"),
        primary_key=True,
        nullable=False,
    )
    ingredient_id: Mapped[UUID] = mapped_column(
        ForeignKey("recipe_ingredient.ingredient_id"),
        primary_key=True,
        nullable=False,
    )
    language_id: Mapped[UUID] = mapped_column(
        ForeignKey("language.id", ondelete=CASCADE),
        primary_key=True,
        nullable=False,
    )
    note: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    brand_recommendation: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    recipe_ingredient: Mapped[RecipeIngredient] = relationship(
        back_populates="translations",
        foreign_keys=[recipe_id, ingredient_id],
    )
    language: Mapped[Language] = relationship(
        back_populates="recipe_ingredient_translations",
    )
