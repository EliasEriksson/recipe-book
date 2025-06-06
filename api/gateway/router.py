import re
from typing import *

import litestar
from litestar.di import Provide
from litestar.params import Parameter

from api.header import Header

from . import routes

pattern = re.compile(r"^\s*(\w{2})(?:-(\w{2}))?(?:\s*;\s*q\s*=\s*([\d.]+)\s*)?$")


def language(
    header_language: Annotated[
        str | None, Parameter(header=Header.Names.accept_language)
    ] = None,
    query_language: Annotated[str | None, Parameter(query="language")] = None,
) -> Generator[str | None, None, None]:
    if query_language == "original":
        yield
    else:
        languages: list[tuple[str, float]] = []
        if query_language:
            languages.append(parse_language(query_language))
        if header_language:
            for language in header_language.split(","):
                if parsed := parse_language(language):
                    languages.append(parsed)
        language_priority = [
            language
            for language, _ in sorted(
                languages, key=lambda languages: languages[1], reverse=True
            )
        ]
        yield language_priority[0] if language_priority else None


def parse_language(language: str) -> tuple[str, float] | None:
    if match := pattern.match(language):
        groups = match.groups()
        return groups[0], 1 if not groups[2] else float(groups[2])
    return None


router = litestar.Router(
    dependencies={"language_code": Provide(language)},
    path="/api/",
    route_handlers=[
        routes.router,
    ],
)
