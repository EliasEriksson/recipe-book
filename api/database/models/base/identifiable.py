from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Uuid
from sqlalchemy import text
from uuid import UUID


class Identifiable(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
