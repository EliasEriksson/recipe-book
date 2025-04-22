import uuid

import litestar


class Controller(litestar.Controller):
    @litestar.get("/")
    async def fetch(self, id: uuid.UUID) -> str:
        return f"/api/recipes/{id}/ingredients/"
