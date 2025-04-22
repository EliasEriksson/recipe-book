from __future__ import annotations

from typing import *
from uuid import UUID

from ..identifiable import IdentityProtocol
from .creatable import Creatable, CreateProtocol


class UnitProtocol(CreateProtocol, IdentityProtocol, Protocol): ...


class Unit(Creatable):
    id: UUID

    @classmethod
    def create(cls, unit: IdentityProtocol, translation: CreateProtocol) -> Unit:
        return cls(
            id=unit.id,
            language_id=translation.language_id,
            name=translation.name,
            symbol=translation.symbol,
        )
