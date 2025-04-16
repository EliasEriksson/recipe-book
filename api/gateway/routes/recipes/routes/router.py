import litestar
from . import ingredients

router = litestar.Router(
    path="/{recipe_id:uuid}/",
    route_handlers=[
        ingredients.router,
    ],
)
