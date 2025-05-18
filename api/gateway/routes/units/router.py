import litestar

from . import routes
from .controller import Controller

router = litestar.Router(
    path="/units/",
    tags=["units"],
    route_handlers=[
        Controller,
        routes.router,
    ],
)
