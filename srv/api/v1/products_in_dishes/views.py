from http import HTTPStatus

from aiohttp import web
from aiohttp_apispec import docs, json_schema, querystring_schema, match_info_schema

from srv.api.base.views import BaseView
from srv.schemas import base as schemas
from srv.services.products_in_dishes import ProductsInDishesService


tags = ["Products in dishes"]
service = ProductsInDishesService()


class ProductsInDishesView(BaseView):
    @docs(
        tags=tags,
        summary="Добавить продукт в блюдо",
        responses=BaseView.BASE_DOCS_RESPONSES | {HTTPStatus.OK: {"description": HTTPStatus.OK.phrase}}
    )
    @match_info_schema(schema=schemas.DishID)
    @json_schema(schemas.ProductInDish)
    async def post(self) -> web.Response:
        body: dict = self.request["json"]
        body["dish"] = self.request["match_info"]["id"]
        await service.add_product_in_dish(self.pg_conn, body)
        return web.Response()

    @docs(
        tags=tags,
        summary="Получить продукты в блюде",
        responses=BaseView.BASE_DOCS_RESPONSES | {
            HTTPStatus.OK: {"description": HTTPStatus.OK.phrase, "schema": schemas.ProductInDishResponse(many=True)}
        }
    )
    @match_info_schema(schema=schemas.DishID)
    async def get(self) -> web.Response:
        match_info: dict = self.request["match_info"]
        if resp := await service.get_products_in_dishes(self.pg_conn, match_info["id"]):
            return web.json_response(text=schemas.ProductInDishResponse(many=True).dumps(resp))
        return web.Response(status=HTTPStatus.NO_CONTENT)
    
    @docs(
        tags=tags,
        summary="Удалить продукт из блюда",
        responses=BaseView.BASE_DOCS_RESPONSES | {HTTPStatus.OK: {"description": HTTPStatus.OK.phrase}}
    )
    @match_info_schema(schema=schemas.DishID)
    @querystring_schema(schemas.DeleteProductInDish)
    async def delete(self) -> web.Response:
        match_info: dict = self.request["match_info"]
        query: dict = self.request["querystring"]
        await service.delete_product_in_dish(self.pg_conn, match_info["id"], query["id"])
        return web.Response(status=HTTPStatus.OK)
