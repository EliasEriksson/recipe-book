from typing import *
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import DateTime
from sqlalchemy import Uuid
from datetime import datetime
from datetime import timezone
from uuid import UUID
from ..constants import gen_random_uuid
from babel.dates import format_datetime


def format(datetime: datetime) -> str:
    return f"{format_datetime(datetime, "EEE, d MMM y HH:mm:ss", tzinfo=timezone.utc, locale="en")} GMT"

class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
    )
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
    )

    @property
    def last_modified(self) -> str:
        return format(self.modified)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __setattr__(self, key: str, value: Any):
        if (
            not key.startswith("_") and
            key != "modified"
            and self.modified is not None
            and getattr(self, key) != value
        ):
            self.modified = datetime.now(tz=timezone.utc)
        return super().__setattr__(key, value)


class Identifiable(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=gen_random_uuid,
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
