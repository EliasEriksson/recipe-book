import litestar

from . import routes
from .controller import Controller

router = litestar.Router(
    path="/recipes/",
    tags=["recipes"],
    route_handlers=[
        Controller,
        routes.router,
    ],
)
