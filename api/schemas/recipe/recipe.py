from __future__ import annotations

from typing import *
from uuid import UUID

from ..identifiable import IdentityProtocol
from .creatable import (
    CreateProtocol,
    RecipeCreatable,
    SharedRecipeCreatableProtocol,
    TranslatedRecipeCreatableProtocol,
)


class RecipeProtocol(CreateProtocol, IdentityProtocol, Protocol): ...


class SharedRecipeProtocol(
    IdentityProtocol, SharedRecipeCreatableProtocol, Protocol
): ...


class TranslatedRecipeProtocol(TranslatedRecipeCreatableProtocol, Protocol): ...


class Recipe(RecipeCreatable):
    id: UUID

    @classmethod
    def create(
        cls, recipe: SharedRecipeProtocol, translation: TranslatedRecipeProtocol
    ) -> Recipe:
        return cls(
            id=recipe.id,
            language_id=translation.language_id,
            name=translation.name,
        )
