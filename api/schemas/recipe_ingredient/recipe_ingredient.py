from __future__ import annotations

from typing import *
from uuid import UUID

from .creatable import (
    RecipeIngredientCreatable,
    SharedRecipeIngredientCreatableProtocol,
    TranslatedRecipeIngredientCreatableProtocol,
)


class SharedRecipeIngredientProtocol(
    SharedRecipeIngredientCreatableProtocol, Protocol
): ...


class TranslatedRecipeIngredientProtocol(
    TranslatedRecipeIngredientCreatableProtocol, Protocol
): ...


class RecipeIngredientProtocol(
    SharedRecipeIngredientProtocol, TranslatedRecipeIngredientProtocol, Protocol
): ...


class RecipeIngredient(RecipeIngredientCreatable):

    @classmethod
    def create(
        cls,
        shared: SharedRecipeIngredientProtocol,
        translation: TranslatedRecipeIngredientProtocol,
    ) -> Self:
        return cls(
            recipe_id=shared.recipe_id,
            ingredient_id=shared.ingredient_id,
            unit_id=shared.unit_id,
            language_id=translation.language_id,
            amount=shared.amount,
            note=translation.note,
            brand_recommendation=translation.brand_recommendation,
        )
