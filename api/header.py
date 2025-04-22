from typing import *
from urllib.parse import urljoin
from litestar import Request
from math import ceil
from datetime import datetime
from datetime import timezone
from .shared.iterable import Iterable
from babel.dates import format_datetime
from sqlalchemy.orm import Mapped
from . import schemas
from uuid import UUID


def format(datetime: datetime) -> str:
    return f"{format_datetime(datetime, "EEE, d MMM y HH:mm:ss", tzinfo=timezone.utc, locale="en")} GMT"


class Translatable(Protocol):
    language_id: UUID | Mapped[UUID]


class Header:
    class Names(Iterable):
        user_agent = "User-Agent"
        authorization = "Authorization"
        www_authenticate = "WWW-Authenticate"
        content_type = "Content-Type"
        last_modified = "Last-Modified"
        accept_language = "Accept-Language"
        link = "Link"

    @classmethod
    def last_modified(
        cls,
        datetime: datetime,
    ) -> Dict[str, str]:
        return {cls.Names.last_modified: format(datetime)}

    @classmethod
    def paging_links(
        cls,
        request: Request,
        limit: int,
        offset: int,
        count: int,
    ) -> Dict[str, str]:
        url = str(request.url)
        last = ceil(count / limit) - 1
        return {
            cls.Names.link: ", ".join(
                link
                for link in (
                    f'<{urljoin(url, f"?limit={limit}&offset={0}")}> rel="first"',
                    (
                        f'<{urljoin(url, f"?limit={limit}&offset={offset - 1}")}> rel="prev"'
                        if offset > 0
                        else None
                    ),
                    (
                        f'<{urljoin(url, f"?limit={limit}&offset={offset + 1}")}> rel="next"'
                        if offset != last
                        else None
                    ),
                    f'<{urljoin(url, f"?limit={limit}&offset={last}")}> rel="last"',
                )
                if link is not None
            )
        }

    @classmethod
    def translations_links(
        cls,
        request: Request,
        translatable: Translatable,
        languages: List[schemas.Language],
    ) -> Dict[str, str]:
        url = str(request.url)
        return {
            cls.Names.link: ", ".join(
                (
                    f'<{urljoin(url, str(language.id))}>; rel="alternate"; hreflang="{language.code}"'
                    for language in languages
                    if language.id != translatable.language_id
                )
            )
        }
