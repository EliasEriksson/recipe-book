from typing import *
import litestar
from litestar import Response
from litestar.params import Parameter
from litestar.exceptions import NotFoundException
from litestar.exceptions import ClientException
from uuid import UUID
from api.headers import Headers
from api import schemas
from api.database import Database


class Controller(litestar.Controller):
    @litestar.get("/")
    async def list(
        self,
        language_code: str | None,
        offset: Annotated[int, Parameter(query="offset")] = 0,
        limit: Annotated[int, Parameter(query="limit")] = 20,
    ) -> Response[List[schemas.Recipe]]:
        async with Database() as client:
            page = await client.recipes.list(language_code, offset, limit)
        return Response(
            [
                schemas.Recipe.create(result.recipe, result.translation)
                for result in page.results
            ]
        )

    @litestar.get("/{id:uuid}/languages/{language_id:uuid}")
    async def fetch(self, id: UUID, language_id: UUID) -> Response[schemas.Recipe]:
        async with Database() as client:
            result = await client.recipes.fetch_by_id(id, language_id)
        if not result:
            raise NotFoundException()
        return Response(
            schemas.Recipe.create(result.recipe, result.translation),
            headers={Headers.last_modified: result.last_modified},
        )

    @litestar.post("/")
    async def create(self, data: schemas.recipe.Creatable) -> Response[schemas.Recipe]:
        async with Database() as client:
            result = await client.recipes.create(data)
        return Response(
            schemas.Recipe.create(result.recipe, result.translation),
            headers={Headers.last_modified: result.last_modified},
        )

    @litestar.put("/{id:uuid}/languages/{language_id:uuid}")
    async def change(
        self, id: UUID, language_id: UUID, data: schemas.Recipe
    ) -> Response[schemas.Recipe]:
        if data.id != id or data.language_id != language_id:
            raise ClientException()
        async with Database() as client:
            result = await client.recipes.update(id, data)
        return Response(
            schemas.Recipe.create(result.recipe, result.translation),
            headers={Headers.last_modified: result.last_modified},
        )

    @litestar.delete("/{id:uuid}/languages/{language_id:uuid}")
    async def delete(self) -> None:
        pass
