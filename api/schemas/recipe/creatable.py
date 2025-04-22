from typing import *
from uuid import UUID

import msgspec
from sqlalchemy.orm import Mapped


class CreateProtocol(Protocol):
    language_id: UUID | Mapped[UUID]
    name: str | Mapped[str]


class Creatable(msgspec.Struct):
    language_id: UUID
    name: str
