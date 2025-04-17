from __future__ import annotations
import msgspec
from typing import *
from ..base import Base


class LanguageCreatable(Base):
    code: Annotated[
        str, msgspec.Meta(min_length=2, max_length=2, pattern=r"^[a-z]{2}$")
    ]
