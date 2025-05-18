import litestar

from . import routes
from .controller import Controller

router = litestar.Router(
    path="/units/",
    tags=["Units"],
    route_handlers=[
        Controller,
        routes.router,
    ],
)
