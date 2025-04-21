from typing import *
from math import floor
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
        limit: int,
        offset: int,
        count: int,
    ) -> Dict[str, str]:
        return {
            cls.Names.link: ", ".join(
                (
                    f'<?limit={limit}&offset={0}>; rel="first"',
                    f'<?limit={limit}&offset={offset - 1}>; rel="prev"',
                    f'<?limit={limit}&offset={offset + 1}>; rel="next"',
                    f'<?limit={limit}&offset={floor(count / limit)}; rel="last">',
                )
            )
        }

    @classmethod
    def translations_links(
        cls,
        translatable: Translatable,
        languages: List[schemas.Language],
    ) -> Dict[str, str]:
        return {
            cls.Names.link: ", ".join(
                (
                    f'<../{language.id}>; rel="alternate"; hreflang="{language.code}"'
                    for language in languages
                    if language.id != translatable.language_id
                )
            )
        }
