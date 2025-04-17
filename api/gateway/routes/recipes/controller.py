import litestar
from litestar import Response
import uuid
from api.headers import Headers
from api import schemas
from api.database import Database


class Controller(litestar.Controller):
    @litestar.get("/")
    async def fetch(self, recipe_id: uuid.UUID) -> str:
        return f"/api/recipes/{recipe_id}"

    @litestar.post("/")
    async def create(self, data: schemas.recipe.Creatable) -> Response[schemas.Recipe]:
        async with Database() as client:
            recipe, translation = await client.recipes.create(data)
        return Response(
            schemas.Recipe.create(recipe, translation),
            headers={
                Headers.last_modified: (
                    recipe.last_modified
                    if recipe.modified > translation.modified
                    else translation.last_modified
                )
            },
        )
