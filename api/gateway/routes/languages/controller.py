from typing import *
from uuid import UUID

import litestar
from litestar import Request, Response
from litestar.exceptions.http_exceptions import ClientException, NotFoundException
from litestar.params import Parameter

from api import schemas
from api.database import Database
from api.header import Header


class Controller(litestar.Controller):
    description = "Delete all data related to this recipe. "

    @litestar.get(
        "/",
        summary="List all available languages.",
    )
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

    @litestar.get(
        "/{id:uuid}",
        summary="Fetch a specified language.",
    )
    async def fetch(self, id: UUID) -> Response[schemas.Language]:
        async with Database() as client:
            result = await client.languages.fetch_by_id(id)
        if not result:
            raise NotFoundException()
        return Response(
            schemas.Language.create(result.language),
            headers=Header.last_modified(result.modified),
        )

    @litestar.post(
        "/",
        summary="Create a new language.",
    )
    async def create(
        self, data: schemas.language.LanguageCreatable
    ) -> Response[schemas.Language]:
        async with Database() as client:
            result = await client.languages.create(data)
        return Response(
            schemas.Language.create(result.language),
            headers=Header.last_modified(result.modified),
        )

    @litestar.put(
        "/{id:uuid}",
        summary="Update a specified language.",
    )
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

    @litestar.delete(
        "/{id:uuid}",
        summary="Delete the specified language.",
        description="Will delete all data that uses this language.",
    )
    async def delete(self, id: UUID) -> None:
        async with Database() as client:
            result = await client.languages.delete(id)
        if result == 0:
            raise NotFoundException()
