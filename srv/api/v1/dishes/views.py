from http import HTTPStatus

from aiohttp import web
from aiohttp_apispec import docs, json_schema

from srv.api.base.views import BaseView
from srv.schemas import base as schemas
from srv.services.dishes import DishesService


tags = ["Dishes"]
service = DishesService()


class DishesView(BaseView):
    @docs(
        tags=tags,
        summary="Создать/обновить блюдо",
        responses=BaseView.BASE_DOCS_RESPONSES | {HTTPStatus.OK: {"description": HTTPStatus.OK.phrase}}
    )
    @json_schema(schemas.Dish)
    async def post(self) -> web.Response:
        body = self.request["json"]
        await service.create_or_update_dish(self.pg_conn, body)
        return web.Response()

    @docs(
        tags=tags,
        summary="Получить блюда",
        responses=BaseView.BASE_DOCS_RESPONSES | {
            HTTPStatus.OK: {"description": HTTPStatus.OK.phrase, "schema": schemas.DishResponse(many=True)}
        }
    )
    async def get(self) -> web.Response:
        if resp := await service.get_dishes(self.pg_conn):
            return web.json_response(text=schemas.DishResponse(many=True).dumps(resp))
        return web.Response(status=HTTPStatus.NO_CONTENT)