import litestar.openapi
from ..configuration import Configuration
from .controller import Controller
from .router import router

configuration = Configuration()


gateway = litestar.Litestar(
    route_handlers=[router],
    openapi_config=litestar.openapi.OpenAPIConfig(
        title="Recipe book",
        version="0.0.0",
        root_schema_site="redoc",
        openapi_controller=Controller,
    ),
    debug=configuration.mode != "prod",
)
