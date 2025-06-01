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


data = [
    {
        "recipe_id": "b4894e26-9bd7-491a-8668-8f0c4f781690",
        "ingredient_id": "5ff0bfaa-d1d3-4a4c-8f22-643b9de87e93",
        "language_id": "c7b82923-1f67-458b-bb23-780c013d461b",
        "unit_id": "ff1575c0-bad6-4944-8946-615c601ea117",
        "amount": 3,
        "note": "",
        "brand_recommendation": "",
    },
    {
        "recipe_id": "b4894e26-9bd7-491a-8668-8f0c4f781690",
        "ingredient_id": "5ff0bfaa-d1d3-4a4c-8f22-643b9de87e93",
        "language_id": "c7b82923-1f67-458b-bb23-780c013d461b",
        "unit_id": "ff1575c0-bad6-4944-8946-615c601ea117",
        "amount": 3,
        "note": "",
        "brand_recommendation": "",
    },
    {
        "recipe_id": "b4894e26-9bd7-491a-8668-8f0c4f781690",
        "ingredient_id": "023c12ce-67af-4d44-bcd4-1a3f9a09f1f0",
        "language_id": "c7b82923-1f67-458b-bb23-780c013d461b",
        "unit_id": "ff1575c0-bad6-4944-8946-615c601ea117",
        "amount": 3,
        "note": "",
        "brand_recommendation": "",
    },
    {
        "recipe_id": "b4894e26-9bd7-491a-8668-8f0c4f781690",
        "ingredient_id": "023c12ce-67af-4d44-bcd4-1a3f9a09f1f0",
        "language_id": "c7b82923-1f67-458b-bb23-780c013d461b",
        "unit_id": "ff1575c0-bad6-4944-8946-615c601ea117",
        "amount": 3,
        "note": "",
        "brand_recommendation": "",
    },
]
