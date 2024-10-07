from aiohttp.web import Application

from srv.api.v1.healthy.routes import create_routes as healthy_routes
from srv.api.v1.products.routes import create_routes as products_routes
from srv.web.context import Context


def v1_routes(app: Application, ctx: Context) -> None:
    path_prefix = f"/{ctx.config.name}/api/v1"
    for create_routes in [healthy_routes, products_routes]:
        create_routes(app, path_prefix)