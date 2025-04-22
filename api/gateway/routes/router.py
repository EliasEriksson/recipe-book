import litestar

from . import languages, recipes

router = litestar.Router(
    path="/",
    route_handlers=[
        recipes.router,
        languages.router,
    ],
)
