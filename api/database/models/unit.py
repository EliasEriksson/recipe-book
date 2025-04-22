from __future__ import annotations

from typing import *

from sqlalchemy.orm import Mapped, relationship

from api import schemas

from ..constants import Cascades
from . import base

if TYPE_CHECKING:
    from .unit_translations import UnitTranslation


class Unit(base.Identifiable):
    __tablename__ = "unit"
    translations: Mapped[List[UnitTranslation]] = relationship(
        back_populates="unit",
        cascade=Cascades.default(),
    )

    @classmethod
    def create(cls, _: schemas.unit.CreateProtocol) -> Unit:
        return cls()

    def update(self, recipe: schemas.unit.UnitProtocol) -> Self:
        self.id = recipe.id
        return self
