from __future__ import annotations

from typing import *

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api import schemas

from ..constants import Cascades
from . import base

if TYPE_CHECKING:
    from .unit_translations import UnitTranslation


class Unit(base.Identifiable):
    __tablename__ = "unit"

    symbol: Mapped[str] = mapped_column(
        String(),
        nullable=False,
        unique=True,
    )

    translations: Mapped[List[UnitTranslation]] = relationship(
        back_populates="unit",
        cascade=Cascades.default(),
    )

    @classmethod
    def create(cls, unit: schemas.unit.CreateProtocol) -> Unit:
        return cls(symbol=unit.symbol)

    def update(self, unit: schemas.unit.UnitProtocol) -> Self:
        self.id = unit.id
        self.symbol = unit.symbol
        return self
