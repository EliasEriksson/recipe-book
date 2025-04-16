import litestar
from . import routes

router = litestar.Router(
    path="/api/",
    route_handlers=[
        routes.router,
    ],
)
