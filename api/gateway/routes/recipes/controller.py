from typing import *
import litestar
from litestar import Response
from litestar.exceptions import NotFoundException
from uuid import UUID
from api.headers import Headers
from api import schemas
from api.database import Database


class Controller(litestar.Controller):
    @litestar.get("/")
    async def list(self) -> Response[List[schemas.Recipe]]:
        return Response([])

    @litestar.get("/{id:uuid}")
    async def fetch(self, id: UUID, languages: List[str]) -> Response[schemas.Recipe]:
        async with Database() as client:
            result = await client.recipes.fetch_by_id(id, languages)
        if not result:
            raise NotFoundException()
        return Response(schemas.Recipe.create(result.recipe, result.translation))

    @litestar.post("/")
    async def create(self, data: schemas.recipe.Creatable) -> Response[schemas.Recipe]:
        async with Database() as client:
            result = await client.recipes.create(data)
        return Response(
            schemas.Recipe.create(result.recipe, result.translation),
            headers={Headers.last_modified: result.last_modified},
        )
