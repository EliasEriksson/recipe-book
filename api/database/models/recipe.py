from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from . import base


class User(base.Identifiable):
    __tablename__ = "user"
    name: Mapped[str] = mapped_column(String(), nullable=False)
