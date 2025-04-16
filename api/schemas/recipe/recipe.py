import uuid
from .creatable import Creatable


class Recipe(Creatable):
    id: uuid.UUID
