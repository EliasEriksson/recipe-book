import litestar
from . import recipes

router = litestar.Router(
    path="/",
    route_handlers=[
        recipes.router,
    ],
)
