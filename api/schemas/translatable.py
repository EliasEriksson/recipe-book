from typing import *
from .language import Language


class TranslatableProtocol(Protocol):
    languages: List[Language]
