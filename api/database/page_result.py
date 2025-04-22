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
