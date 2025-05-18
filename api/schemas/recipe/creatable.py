from typing import *
from uuid import UUID

import msgspec
from sqlalchemy.orm import Mapped


class SharedRecipeCreatableProtocol(Protocol): ...


class TranslatedRecipeCreatableProtocol(Protocol):
    language_id: UUID | Mapped[UUID]
    name: str | Mapped[str]


class CreateProtocol(
    SharedRecipeCreatableProtocol, TranslatedRecipeCreatableProtocol, Protocol
): ...


class RecipeCreatable(msgspec.Struct):
    language_id: UUID
    name: str
