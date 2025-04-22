from __future__ import annotations

from typing import *

from sqlalchemy.orm import Mapped, relationship

from api import schemas

from ..constants import Cascades
from . import base

if TYPE_CHECKING:
    from .recipe_translation import RecipeTranslation


class Recipe(base.Identifiable):
    __tablename__ = "recipe"
    translations: Mapped[list[RecipeTranslation]] = relationship(
        back_populates="recipe",
        cascade=Cascades.default(),
    )

    @classmethod
    def create(cls, _: schemas.recipe.CreateProtocol) -> Recipe:
        return cls()

    def update(self, recipe: schemas.recipe.RecipeProtocol) -> Recipe:
        self.id = recipe.id
        return self
