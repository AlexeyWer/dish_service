from http import HTTPStatus

from aiohttp import web
from aiohttp_apispec import docs, json_schema, querystring_schema

from srv.api.base.views import BaseView
from srv.schemas import base as schemas
from srv.services.products import ProductsService


tags = ["Products"]
service = ProductsService()


class ProductsView(BaseView):
    @docs(
        tags=tags,
        summary="Создать/обновить продукт",
        responses=BaseView.BASE_DOCS_RESPONSES | {HTTPStatus.OK: {"description": HTTPStatus.OK.phrase}}
    )
    @json_schema(schemas.Product)
    async def post(self) -> web.Response:
        body = self.request["json"]
        await service.create_or_update_product(self.pg_conn, body)
        return web.Response()

    @docs(
        tags=tags,
        summary="Получить продукты",
        responses=BaseView.BASE_DOCS_RESPONSES | {
            HTTPStatus.OK: {"description": HTTPStatus.OK.phrase, "schema": schemas.ProductResponse(many=True)}
        }
    )
    async def get(self) -> web.Response:
        if resp := await service.get_products(self.pg_conn):
            return web.json_response(text=schemas.ProductResponse(many=True).dumps(resp))
        return web.Response(status=HTTPStatus.NO_CONTENT)

    @docs(
        tags=tags,
        summary="Удалить продукт",
        responses=BaseView.BASE_DOCS_RESPONSES | {HTTPStatus.OK: {"description": HTTPStatus.OK.phrase}}
    )
    @querystring_schema(schemas.DeleteProduct)
    async def delete(self) -> web.Response:
        query: dict = self.request["querystring"]
        await service.delete_product(self.pg_conn, query["pk"], "name", query["name"])
        return web.Response(status=HTTPStatus.OK)
