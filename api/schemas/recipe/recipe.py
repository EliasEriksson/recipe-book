from __future__ import annotations
from typing import *
from .creatable import Creatable
from .creatable import CreateProtocol
from uuid import UUID
from ..identifiable import IdentityProtocol
from ..translatable import TranslatableProtocol
from ..language import Language


class RecipeProtocol(
    CreateProtocol, IdentityProtocol, TranslatableProtocol, Protocol
): ...


class Recipe(Creatable):
    id: UUID
    languages: List[Language]

    # TODO add support for languages
    @classmethod
    def create(cls, recipe: IdentityProtocol, translations: CreateProtocol) -> Recipe:
        return cls(
            id=recipe.id,
            language_id=translations.language_id,
            name=translations.name,
            languages=[],
        )
