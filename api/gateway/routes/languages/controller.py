from typing import *
import litestar
from litestar import Response
from litestar import Request
from litestar.params import Parameter
from litestar.exceptions.http_exceptions import NotFoundException
from litestar.exceptions.http_exceptions import ClientException
from uuid import UUID
from api import schemas
from api.header import Header
from api.database import Database


class Controller(litestar.Controller):
    @litestar.get("/")
    async def list(
        self,
        request: Request,
        limit: Annotated[int, Parameter(query="limit")] = 20,
        offset: Annotated[int, Parameter(query="offset")] = 0,
    ) -> Response[List[schemas.Language]]:
        async with Database() as client:
            result = await client.languages.list(limit, offset)
        return Response(
            [schemas.Language.create(result.language) for result in result.results],
            headers=Header.paging_links(
                request,
                limit,
                offset,
                result.count,
            ),
        )

    @litestar.get("/{id:uuid}")
    async def fetch(self, id: UUID) -> Response[schemas.Language]:
        async with Database() as client:
            result = await client.languages.fetch_by_id(id)
        if not result:
            raise NotFoundException()
        return Response(
            schemas.Language.create(result.language),
            headers=Header.last_modified(result.modified),
        )

    @litestar.post("/")
    async def create(
        self, data: schemas.language.LanguageCreatable
    ) -> Response[schemas.Language]:
        async with Database() as client:
            result = await client.languages.create(data)
        return Response(
            schemas.Language.create(result.language),
            headers=Header.last_modified(result.modified),
        )

    @litestar.put("/{id:uuid}")
    async def update(
        self, id: UUID, data: schemas.language.Language
    ) -> Response[schemas.Language]:
        if data.id != id:
            raise ClientException()
        async with Database() as client:
            result = await client.languages.update(id, data)
        return Response(
            schemas.Language.create(result.language),
            headers=Header.last_modified(result.modified),
        )

    @litestar.delete("/{id:uuid}")
    async def delete(self, id: UUID) -> None:
        async with Database() as client:
            result = await client.languages.delete(id)
        if result == 0:
            raise NotFoundException()
