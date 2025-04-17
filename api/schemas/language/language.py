from __future__ import annotations
from typing import *
from .creatable import LanguageCreatable
from .creatable import CreateProtocol
from uuid import UUID
from ..base import IdentityProtocol


class LanguageProtocol(CreateProtocol, IdentityProtocol, Protocol): ...


class Language(LanguageCreatable):
    id: UUID

    @classmethod
    def create(cls, language: LanguageProtocol) -> Language:
        return cls(
            id=language.id,
            code=language.code,
        )
