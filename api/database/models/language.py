from __future__ import annotations

from typing import *

from sqlalchemy import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api import schemas

from ..constants import Cascades
from . import base

if TYPE_CHECKING:
    from .recipe_translation import RecipeTranslation
    from .unit_translations import UnitTranslation


class CreateProtocol(Protocol):
    code: str


class Language(base.Identifiable):
    __tablename__ = "language"
    code: Mapped[str] = mapped_column(
        CHAR(length=2),
        unique=True,
        nullable=False,
    )
    recipe_translations: Mapped[List[RecipeTranslation]] = relationship(
        back_populates="language",
        cascade=Cascades.default(),
    )
    unit_translations: Mapped[List[UnitTranslation]] = relationship(
        back_populates="language",
        cascade=Cascades.default(),
    )

    @classmethod
    def create(cls, language: CreateProtocol) -> Language:
        return cls(code=language.code)

    def update(self, language: schemas.language.LanguageProtocol) -> Self:
        self.id = language.id
        self.code = language.code
        return self
