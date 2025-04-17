from .creatable import Creatable
from uuid import UUID


class Recipe(Creatable):
    id: UUID
