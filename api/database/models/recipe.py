from __future__ import annotations
from typing import *
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
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
