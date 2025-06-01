from __future__ import annotations

from typing import *
from uuid import UUID

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ... import schemas
from ..constants import CASCADE
from .base import Base

if TYPE_CHECKING:
    from .language import Language
    from .recipe_ingredient import RecipeIngredient


class RecipeIngredientTranslation(Base):
    __tablename__ = "recipe_ingredient_translation"
    recipe_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    ingredient_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    language_id: Mapped[UUID] = mapped_column(
        ForeignKey("language.id", ondelete=CASCADE),
        primary_key=True,
        nullable=False,
    )
    note: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    brand_recommendation: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    recipe_ingredient: Mapped[RecipeIngredient] = relationship(
        back_populates="translations",
        foreign_keys=[recipe_id, ingredient_id],
    )
    language: Mapped[Language] = relationship(
        back_populates="recipe_ingredient_translations",
    )
    __table_args__ = (
        ForeignKeyConstraint(
            [recipe_id, ingredient_id],
            ["recipe_ingredient.recipe_id", "recipe_ingredient.ingredient_id"],
            ondelete=CASCADE,
        ),
    )

    @classmethod
    def create(
        cls,
        recipe_ingredient: RecipeIngredient,
        translation: schemas.recipe_ingredient.CreateProtocol,
    ) -> Self:
        return cls(
            recipe_id=recipe_ingredient.recipe_id,
            ingredient_id=recipe_ingredient.ingredient_id,
            language_id=translation.language_id,
            note=translation.note,
            brand_recommendation=translation.brand_recommendation,
        )
