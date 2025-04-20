from typing import *
import litestar
from litestar import Response
from litestar.exceptions import NotFoundException
from litestar.exceptions import ClientException
from uuid import UUID
from api.headers import Headers
from api import schemas
from api.database import Database


class Controller(litestar.Controller):
    @litestar.get("/")
    async def list(self, language: str | None) -> Response[List[schemas.Recipe]]:
        async with Database() as client:
            results = await client.recipes.list(language)
        return Response(
            [
                schemas.Recipe.create(result.recipe, result.translation)
                for result in results
            ]
        )

    @litestar.get("/{id:uuid}/language/{language_id:uuid}")
    async def fetch(self, id: UUID, language: str) -> Response[schemas.Recipe]:
        async with Database() as client:
            result = await client.recipes.fetch_by_id(id, language)
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

    @litestar.delete("/{id:uuid}/language/{language_id:uuid}")
    async def delete(self) -> None:
        pass
