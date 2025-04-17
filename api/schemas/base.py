from typing import *
import msgspec
from uuid import UUID
from sqlalchemy.orm import Mapped


class Base(msgspec.Struct, rename="camel"): ...


class IdentityProtocol(Protocol):
    id: UUID | Mapped[UUID]
