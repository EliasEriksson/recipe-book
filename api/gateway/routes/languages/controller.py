import litestar
from litestar import Response
from litestar.exceptions.http_exceptions import NotFoundException
from litestar.exceptions.http_exceptions import ClientException
from uuid import UUID
from api import schemas
from api.headers import Headers
from api.database import Database


class Controller(litestar.Controller):
    @litestar.get("/")
    async def list(self) -> Response[list[schemas.Language]]:
        async with Database() as client:
            result = await client.languages.list()
        return Response(
            [schemas.Language.create(language) for language in result],
        )

    @litestar.get("/{language_id:uuid}")
    async def fetch(self, language_id: UUID) -> Response[schemas.Language]:
        async with Database() as client:
            result = await client.languages.fetch_by_id(language_id)
        return Response(
            schemas.Language.create(result),
            headers={Headers.last_modified: result.last_modified},
        )

    @litestar.post("/")
    async def create(
        self, data: schemas.language.LanguageCreatable
    ) -> Response[schemas.Language]:
        async with Database() as client:
            result = await client.languages.create(data)
        return Response(
            schemas.Language.create(result),
            headers={Headers.last_modified: result.last_modified},
        )

    @litestar.put("/{language_id:uuid}")
    async def update(
        self, language_id: UUID, data: schemas.language.Language
    ) -> Response[schemas.Language]:
        if data.id != language_id:
            raise ClientException("ids not matching")
        async with Database() as client:
            result = await client.languages.update(language_id, data)
        return Response(
            schemas.Language.create(result),
            headers={Headers.last_modified: result.last_modified},
        )

    @litestar.delete("/{language_id:uuid}")
    async def delete(self, language_id: UUID) -> None:
        async with Database() as client:
            result = await client.languages.delete_by_id(language_id)
        if result == 0:
            raise NotFoundException("Language not found")
