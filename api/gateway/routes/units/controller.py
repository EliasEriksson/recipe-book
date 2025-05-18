import asyncio
from typing import *
from uuid import UUID

import litestar
from litestar import Request, Response
from litestar.exceptions import ClientException, NotFoundException
from litestar.params import Parameter

from api import schemas
from api.database import Database
from api.header import Header


class Controller(litestar.Controller):
    @litestar.get("/")
    async def list(
        self,
        request: Request,
        language_code: str | None,
        limit: Annotated[int, Parameter(query="limit")] = 20,
        offset: Annotated[int, Parameter(query="offset")] = 0,
    ) -> Response[List[schemas.Unit]]:
        async with Database() as client:
            result = await client.units.list(language_code, limit, offset)
        return Response(
            [
                schemas.Unit.create(result.unit, result.translation)
                for result in result.results
            ],
            headers=Header.paging_links(request, limit, offset, result.count),
        )

    @litestar.get("/{id:uuid}/languages")
    async def list_languages(
        self,
        request: Request,
        id: UUID,
        limit: Annotated[int, Parameter(query="limit")] = 20,
        offset: Annotated[int, Parameter(query="offset")] = 0,
    ) -> Response[List[schemas.Language]]:
        async with Database() as client:
            result = await client.languages.list_by_unit(id, limit, offset)
        return Response(
            [schemas.Language.create(result.language) for result in result.results],
            headers=Header.paging_links(request, limit, offset, result.count),
        )

    @litestar.get("/{id:uuid}/languages/{language_id:uuid}")
    async def fetch(
        self,
        request: Request,
        id: UUID,
        language_id: UUID,
    ) -> Response[schemas.Unit]:
        async with Database() as client:
            result, language_result = await asyncio.gather(
                client.units.fetch_by_id(id, language_id),
                client.languages.list_by_unit(id),
            )
        if not result:
            raise NotFoundException()
        return Response(
            schemas.Unit.create(result.unit, result.translation),
            headers=Header.last_modified(result.modified)
            | Header.translations_links(
                request,
                result.translation,
                [result.language for result in language_result.results],
            ),
        )

    @litestar.post("/")
    async def create(self, data: schemas.unit.Creatable) -> Response[schemas.Unit]:
        async with Database() as client:
            result = await client.units.create(data)
        return Response(
            schemas.Unit.create(result.unit, result.translation),
            headers=Header.last_modified(result.modified),
        )

    @litestar.put("/{id:uuid}/languages/{language_id:uuid}")
    async def change(
        self,
        id: UUID,
        language_id: UUID,
        data: schemas.Unit,
    ) -> Response[schemas.Unit]:
        if data.id != id or data.language_id != language_id:
            raise ClientException()
        async with Database() as client:
            result = await client.units.update(id, data)
        return Response(
            schemas.Unit.create(result.unit, result.translation),
            headers=Header.last_modified(result.modified),
        )

    @litestar.delete("/{id:uuid")
    async def delete(self, id: UUID) -> Response[None]:
        async with Database() as client:
            result = await client.units.delete(id)
        if not result:
            raise NotFoundException()
        return Response(None)

    @litestar.delete("/{id:uuid}/languages/{language_id:uuid}")
    async def delete_translation(self, id: UUID, language_id: UUID) -> Response[None]:
        async with Database() as client:
            result = await client.units.delete_translation(id, language_id)
        if not result:
            raise NotFoundException()
        return Response(None)
