import litestar
from . import recipes
from . import languages

router = litestar.Router(
    path="/",
    route_handlers=[
        recipes.router,
        languages.router,
    ],
)
