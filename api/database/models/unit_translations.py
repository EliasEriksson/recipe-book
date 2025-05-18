from __future__ import annotations

from typing import *
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ... import schemas
from ..constants import CASCADE
from . import base

if TYPE_CHECKING:
    from .language import Language
    from .unit import Unit


class UnitTranslation(base.Base):
    __tablename__ = "unit_translation"

    unit_id: Mapped[UUID] = mapped_column(
        ForeignKey("unit.id", ondelete=CASCADE),
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

    unit: Mapped[Unit] = relationship(
        back_populates="translations",
    )
    language: Mapped[Language] = relationship(
        back_populates="unit_translations",
    )

    @classmethod
    def create(cls, unit: Unit, translation: schemas.unit.CreateProtocol) -> Self:
        return cls(
            unit_id=unit.id,
            language_id=translation.language_id,
            name=translation.name,
        )

    def update(self, unit: schemas.unit.UnitProtocol) -> Self:
        self.unit_id = unit.id
        self.language_id = unit.language_id
        self.name = unit.name
        return self
