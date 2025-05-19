from __future__ import annotations

from typing import *

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api import schemas

from ..constants import Cascades
from . import base

if TYPE_CHECKING:
    from .ingredient_translation import IngredientTranslation


class Ingredient(base.Identifiable):
    __tablename__ = "ingredient"
    translations: Mapped[List[IngredientTranslation]] = relationship(
        back_populates="ingredient",
        cascade=Cascades.default(),
    )

    @classmethod
    def create(cls, _: schemas.ingredient.CreateProtocol) -> Self:
        return cls()

    def update(self, ingredient: schemas.ingredient.IngredientProtocol) -> Self:
        self.id = ingredient.id
        return self
