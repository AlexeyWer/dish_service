from http import HTTPStatus

from aiohttp import web
from aiohttp_apispec import docs

from srv.api.base.views import BaseView


class LivenessView(BaseView):
    @docs(
        tags=["Check server"],
        summary="Проверка работоспособности сервера",
        responses=BaseView.BASE_DOCS_RESPONSES | {HTTPStatus.OK: {"description": HTTPStatus.OK.phrase}}
    )
    async def get(self) -> web.Response:
        return web.Response()


class ReadinessView(BaseView):
    @docs(
        tags=["Check server"],
        summary="Проверка работоспособности используемых сервером баз данных",
        responses=BaseView.BASE_DOCS_RESPONSES | {HTTPStatus.OK: {"description": HTTPStatus.OK.phrase}}
    )
    async def get(self) -> web.Response:
        if not await self.ctx.postgres_accessor.ping():
            raise web.HTTPInternalServerError()
        return web.Response()