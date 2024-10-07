from aiohttp.web import Application

from srv.api.v1.products.views import ProductsView


def create_routes(app: Application, path_prefix: str) -> None:
    app.router.add_view(f"{path_prefix}/products", ProductsView)
