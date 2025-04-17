from __future__ import annotations
from typing import *
from .creatable import LanguageCreatable
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped


class LanguageProtocol(Protocol):
    id: UUID | Mapped[UUID]
    code: str | Mapped[str]


class Language(LanguageCreatable):
    id: UUID

    @classmethod
    def create(cls, language: LanguageProtocol) -> Language:
        return cls(
            id=language.id,
            code=language.code,
        )
