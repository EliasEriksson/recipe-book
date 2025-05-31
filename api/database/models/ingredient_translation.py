from __future__ import annotations

from typing import *
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ... import schemas
from ..constants import CASCADE
from .base import Base

if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .language import Language


class IngredientTranslation(Base):
    __tablename__ = "ingredient_translation"
    ingredient_id: Mapped[UUID] = mapped_column(
        ForeignKey("ingredient.id", ondelete=CASCADE),
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
    ingredient: Mapped[Ingredient] = relationship(
        back_populates="translations",
    )
    language: Mapped[Language] = relationship(
        back_populates="ingredient_translations",
    )

    @classmethod
    def create(
        cls, ingredient: Ingredient, translation: schemas.ingredient.CreateProtocol
    ) -> Self:
        return cls(
            ingredient_id=ingredient.id,
            language_id=translation.language_id,
            name=translation.name,
        )

    def update(self, ingredient: schemas.ingredient.IngredientProtocol) -> Self:
        self.ingredient_id = ingredient.id
        self.language_id = ingredient.language_id
        self.name = ingredient.name
        return self
