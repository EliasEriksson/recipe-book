from __future__ import annotations

from typing import *
from uuid import UUID

from ..identifiable import IdentityProtocol
from .creatable import (
    CreateProtocol,
    SharedUnitCreatableProtocol,
    TranslatedUnitCreatableProtocol,
    UnitCreatable,
)


class UnitProtocol(CreateProtocol, IdentityProtocol, Protocol): ...


class SharedUnitProtocol(IdentityProtocol, SharedUnitCreatableProtocol, Protocol): ...


class TranslatedUnitProtocol(TranslatedUnitCreatableProtocol, Protocol): ...


class Unit(UnitCreatable):
    id: UUID

    @classmethod
    def create(
        cls, unit: SharedUnitProtocol, translation: TranslatedUnitProtocol
    ) -> Self:
        return cls(
            id=unit.id,
            symbol=unit.symbol,
            language_id=translation.language_id,
            name=translation.name,
        )
