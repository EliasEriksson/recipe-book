from typing import *
from uuid import UUID

import msgspec
from sqlalchemy.orm import Mapped


class SharedIngredientCreatableProtocol(Protocol): ...


class TranslatedIngredientCreatableProtocol(Protocol):
    language_id: UUID | Mapped[UUID]
    name: str | Mapped[str]


class CreateProtocol(
    SharedIngredientCreatableProtocol, TranslatedIngredientCreatableProtocol, Protocol
): ...


class IngredientCreatable(msgspec.Struct):
    language_id: UUID
    name: str
