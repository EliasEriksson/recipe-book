import litestar

from . import routes
from .controller import Controller

router = litestar.Router(
    path="/recipes/",
    tags=["Recipes"],
    route_handlers=[
        Controller,
        routes.router,
    ],
)
