import msgspec
from uuid import UUID


class Creatable(msgspec.Struct):
    language_id: UUID
    name: str
