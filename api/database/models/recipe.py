from __future__ import annotations

from typing import *

from sqlalchemy.orm import Mapped, relationship

from api import schemas

from ..constants import Cascades
from .base import Identifiable

if TYPE_CHECKING:
    from .recipe_ingredient import RecipeIngredient
    from .recipe_translation import RecipeTranslation


class Recipe(Identifiable):
    __tablename__ = "recipe"
    recipe_ingredients: Mapped[List[RecipeIngredient]] = relationship(
        back_populates="recipe",
        cascade=Cascades.default(),
    )
    translations: Mapped[List[RecipeTranslation]] = relationship(
        back_populates="recipe",
        cascade=Cascades.default(),
    )

    @classmethod
    def create(cls, _: schemas.recipe.CreateProtocol) -> Self:
        return cls()

    def update(self, recipe: schemas.recipe.RecipeProtocol) -> Self:
        self.id = recipe.id
        return self
