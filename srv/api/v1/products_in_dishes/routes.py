from aiohttp.web import Application

from srv.api.v1.products_in_dishes.views import ProductsInDishesView


def create_routes(app: Application, path_prefix: str) -> None:
    app.router.add_view(f"{path_prefix}/dishes/products", ProductsInDishesView)
