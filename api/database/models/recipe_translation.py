from __future__ import annotations
from typing import *
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import String
from uuid import UUID
from . import base
from ..constants import CASCADE
from ... import schemas

if TYPE_CHECKING:
    from .recipe import Recipe
    from .language import Language


class RecipeTranslation(base.Base):
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
        String(),
        nullable=False,
    )
    recipe: Mapped[Recipe] = relationship(
        back_populates="translations",
    )
    language: Mapped[Language] = relationship(
        back_populates="recipe_translations",
    )

    @classmethod
    def create(
        cls, recipe: Recipe, translation: schemas.recipe.CreateProtocol
    ) -> RecipeTranslation:
        return cls(
            recipe_id=recipe.id,
            language_id=translation.language_id,
            name=translation.name,
        )

    def update(self, recipe: schemas.recipe.RecipeProtocol) -> RecipeTranslation:
        self.recipe_id = recipe.id
        self.language_id = recipe.language_id
        self.name = recipe.name
        return self
