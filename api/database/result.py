from datetime import datetime
from typing import *


class PageResult[T]:
    limit: int | None
    offset: int | None
    results: List[T]

    def __init__(
        self,
        limit: int | None,
        offset: int | None,
        count: int,
        results: List[T],
    ) -> None:
        self.limit = limit
        self.offset = offset
        self.count = count
        self.results = results


class TranslatedResult[TShared, TTranslation]:
    shared: TShared

    def __init__(self, shared: TShared, translation: TTranslation) -> None:
        self.shared = shared
        self.translation = translation

    @property
    def modified(self) -> datetime:
        return (
            self.shared.modified
            if self.shared.modified > self.translation.modified
            else self.translation.modified
        )
