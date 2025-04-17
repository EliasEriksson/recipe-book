from __future__ import annotations
from typing import *
import msgspec
from sqlalchemy.orm import Mapped
from ..base import Base


class CreateProtocol(Protocol):
    code: str | Mapped[str]


class LanguageCreatable(Base):
    code: Annotated[
        str, msgspec.Meta(min_length=2, max_length=2, pattern=r"^[a-z]{2}$")
    ]
