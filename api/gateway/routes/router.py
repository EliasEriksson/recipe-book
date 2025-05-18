import litestar

from . import languages, recipes, units

router = litestar.Router(
    path="/",
    route_handlers=[
        recipes.router,
        languages.router,
        units.router,
    ],
)
