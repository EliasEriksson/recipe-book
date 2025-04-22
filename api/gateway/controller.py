import litestar.openapi

from .router import router


class Controller(litestar.openapi.OpenAPIController):
    path = router.path
