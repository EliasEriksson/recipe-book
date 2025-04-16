import litestar
import uuid


class Controller(litestar.Controller):
    @litestar.get("/")
    async def fetch(self, id: uuid.UUID) -> str:
        return f"/api/recipes/{id}/ingredients/"
