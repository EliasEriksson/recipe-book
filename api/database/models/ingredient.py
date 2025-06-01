from __future__ import annotations

from typing import *

from sqlalchemy.orm import Mapped, relationship

from api import schemas

from ..constants import Cascades
from .base import Identifiable

if TYPE_CHECKING:
    from .ingredient_translation import IngredientTranslation
    from .recipe_ingredient import RecipeIngredient


class Ingredient(Identifiable):
    __tablename__ = "ingredient"
    recipe_ingredients: Mapped[List[RecipeIngredient]] = relationship(
        back_populates="ingredient",
        cascade=Cascades.default(),
    )
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
