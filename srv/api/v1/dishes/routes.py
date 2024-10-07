from aiohttp.web import Application

from srv.api.v1.dishes.views import DishesView


def create_routes(app: Application, path_prefix: str) -> None:
    app.router.add_view(f"{path_prefix}/dishes", DishesView)
