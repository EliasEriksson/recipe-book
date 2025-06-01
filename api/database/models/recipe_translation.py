from __future__ import annotations

from typing import *
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ... import schemas
from ..constants import CASCADE
from .base import Base

if TYPE_CHECKING:
    from .language import Language
    from .recipe import Recipe


class RecipeTranslation(Base):
    __tablename__ = "recipe_translation"
    recipe_id: Mapped[UUID] = mapped_column(
        ForeignKey("recipe.id", ondelete=CASCADE),
        primary_key=True,
        nullable=False,
    )
    language_id: Mapped[UUID] = mapped_column(
        ForeignKey("language.id", ondelete=CASCADE),
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    recipe: Mapped[Recipe] = relationship(
        back_populates="translations",
    )
    language: Mapped[Language] = relationship(
        back_populates="recipe_translations",
    )

    @classmethod
    def create(cls, recipe: Recipe, translation: schemas.recipe.CreateProtocol) -> Self:
        return cls(
            recipe_id=recipe.id,
            language_id=translation.language_id,
            name=translation.name,
        )

    def update(self, recipe: schemas.recipe.RecipeProtocol) -> Self:
        self.recipe_id = recipe.id
        self.language_id = recipe.language_id
        self.name = recipe.name
        return self
