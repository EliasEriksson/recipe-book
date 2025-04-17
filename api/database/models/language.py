from __future__ import annotations
from typing import *
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import CHAR
from . import base
from ..constants import Cascades
from api import schemas

if TYPE_CHECKING:
    from .recipe_translation import RecipeTranslation


class CreateProtocol(Protocol):
    code: str


class Language(base.Identifiable):
    __tablename__ = "language"
    code: Mapped[str] = mapped_column(
        CHAR(length=2),
        unique=True,
        nullable=False,
    )
    recipe_translations: Mapped[list[RecipeTranslation]] = relationship(
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
