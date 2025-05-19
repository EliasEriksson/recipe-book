from __future__ import annotations

from typing import *
from uuid import UUID

from ..identifiable import IdentityProtocol
from .creatable import (
    CreateProtocol,
    IngredientCreatable,
    SharedIngredientCreatableProtocol,
    TranslatedIngredientCreatableProtocol,
)


class IngredientProtocol(CreateProtocol, IdentityProtocol, Protocol): ...


class SharedIngredientProtocol(
    IdentityProtocol, SharedIngredientCreatableProtocol, Protocol
): ...


class TranslatedIngredientProtocol(TranslatedIngredientCreatableProtocol, Protocol): ...


class Ingredient(IngredientCreatable):
    id: UUID

    @classmethod
    def create(
        cls,
        ingredient: SharedIngredientProtocol,
        translation: TranslatedIngredientProtocol,
    ) -> Self:
        return cls(
            id=ingredient.id,
            language_id=translation.language_id,
            name=translation.name,
        )
