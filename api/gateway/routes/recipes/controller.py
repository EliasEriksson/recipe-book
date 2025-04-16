import litestar
import uuid


class Controller(litestar.Controller):
    @litestar.get("/")
    async def fetch(self, recipe_id: uuid.UUID) -> str:
        return f"/api/recipes/{recipe_id}"
