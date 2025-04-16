# import pydantic
import uuid
from ..base import Base


class Creatable(Base):
    language_id: uuid.UUID
    # name: str = pydantic.Field()
