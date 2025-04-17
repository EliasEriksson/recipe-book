from typing import *
import msgspec
from sqlalchemy.orm import Mapped
from uuid import UUID


class CreateProtocol(Protocol):
    language_id: UUID | Mapped[UUID]
    name: str | Mapped[str]


class Creatable(msgspec.Struct):
    language_id: UUID
    name: str
