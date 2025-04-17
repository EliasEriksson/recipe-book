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

    @litestar.get("/{id:uuid}")
    async def fetch(self, id: UUID) -> Response[schemas.Language]:
        async with Database() as client:
            result = await client.languages.fetch_by_id(id)
        if not result:
            raise NotFoundException()
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

    @litestar.put("/{id:uuid}")
    async def update(
        self, id: UUID, data: schemas.language.Language
    ) -> Response[schemas.Language]:
        if data.id != id:
            raise ClientException("ids not matching")
        async with Database() as client:
            result = await client.languages.update(id, data)
        return Response(
            schemas.Language.create(result),
            headers={Headers.last_modified: result.last_modified},
        )

    @litestar.delete("/{id:uuid}")
    async def delete(self, id: UUID) -> None:
        async with Database() as client:
            result = await client.languages.delete_by_id(id)
        if result == 0:
            raise NotFoundException("Language not found")
