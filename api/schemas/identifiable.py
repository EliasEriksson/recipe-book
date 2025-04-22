from typing import *
from uuid import UUID

from sqlalchemy.orm import Mapped


class IdentityProtocol(Protocol):
    id: UUID | Mapped[UUID]
