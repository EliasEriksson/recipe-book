from __future__ import annotations

from typing import *
from uuid import UUID

from ..identifiable import IdentityProtocol
from .creatable import CreateProtocol, LanguageCreatable


class LanguageProtocol(CreateProtocol, IdentityProtocol, Protocol): ...


class Language(LanguageCreatable):
    id: UUID

    @classmethod
    def create(cls, language: LanguageProtocol) -> Language:
        return cls(
            id=language.id,
            code=language.code,
        )
