from __future__ import annotations

from typing import *
from uuid import UUID

from ..identifiable import IdentityProtocol
from .creatable import Creatable, CreateProtocol


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
