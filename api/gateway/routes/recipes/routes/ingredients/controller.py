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
        recipe_id: UUID,
        language_code: str | None,
        limit: Annotated[int, Parameter(query="limit")] = 20,
        offset: Annotated[int, Parameter(query="offset")] = 0,
    ) -> Response[List[schemas.RecipeIngredient]]:
        async with Database() as client:
            result = await client.recipe_ingredients.list(
                recipe_id, language_code, limit, offset
            )
        return Response(
            [
                schemas.RecipeIngredient.create(result.shared, result.translation)
                for result in result.results
            ]
        )

    @litestar.get("/{ingredient_id:uuid}/languages/{language_id:uuid}")
    async def fetch(
        self, recipe_id: UUID, ingredient_id: UUID, language_id: UUID
    ) -> Response[schemas.RecipeIngredient]:
        async with Database() as client:
            result = await client.recipe_ingredients.fetch_by_id(
                recipe_id, ingredient_id, language_id
            )
        return Response(
            schemas.RecipeIngredient.create(result.shared, result.translation)
        )
