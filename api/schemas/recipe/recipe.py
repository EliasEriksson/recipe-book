from __future__ import annotations
from typing import *
from .creatable import Creatable
from .creatable import CreateProtocol
from uuid import UUID
from ..identifiable import IdentityProtocol


class RecipeProtocol(CreateProtocol, IdentityProtocol, Protocol): ...


class Recipe(Creatable):
    id: UUID

    # TODO add support for languages
    @classmethod
    def create(cls, recipe: IdentityProtocol, translations: CreateProtocol) -> Recipe:
        return cls(
            id=recipe.id,
            language_id=translations.language_id,
            name=translations.name,
        )
