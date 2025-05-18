from typing import *
from uuid import UUID

import msgspec
from sqlalchemy.orm import Mapped


class SharedUnitCreatableProtocol(Protocol):
    symbol: str | Mapped[str]


class TranslatedUnitCreatableProtocol(Protocol):
    language_id: UUID | Mapped[UUID]
    name: str | Mapped[str]


class CreateProtocol(
    SharedUnitCreatableProtocol, TranslatedUnitCreatableProtocol, Protocol
): ...


class UnitCreatable(msgspec.Struct):
    language_id: UUID
    name: str
    symbol: str
