from typing import *
from uuid import UUID

import msgspec
from sqlalchemy.orm import Mapped


class SharedRecipeIngredientCreatableProtocol(Protocol):
    recipe_id: UUID | Mapped[UUID]
    ingredient_id: UUID | Mapped[UUID]
    unit_id: UUID | Mapped[UUID]
    amount: int | Mapped[int]


class TranslatedRecipeIngredientCreatableProtocol(Protocol):
    recipe_id: UUID | Mapped[UUID]
    ingredient_id: UUID | Mapped[UUID]
    language_id: UUID | Mapped[UUID]
    note: str | Mapped[str]
    brand_recommendation: str | Mapped[str]


class CreateProtocol(
    SharedRecipeIngredientCreatableProtocol,
    TranslatedRecipeIngredientCreatableProtocol,
    Protocol,
): ...


class RecipeIngredientCreatable(msgspec.Struct):
    recipe_id: UUID
    ingredient_id: UUID
    language_id: UUID
    unit_id: UUID
    amount: int
    note: str
    brand_recommendation: str
