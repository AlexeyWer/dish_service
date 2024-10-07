from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncConnection
from aiohttp.web import View, Request, Response
from aiohttp_cors import CorsViewMixin

from srv.api.base.schemas import BaseSchema
from srv.web.context import Context



class BaseView(View, CorsViewMixin):
    BASE_DOCS_RESPONSES = {
        HTTPStatus.UNPROCESSABLE_ENTITY: {"description": HTTPStatus.UNPROCESSABLE_ENTITY.phrase},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": HTTPStatus.INTERNAL_SERVER_ERROR.phrase},
    }

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.ctx: Context = getattr(request.app, "context")
        self.pg_conn: AsyncConnection = getattr(request, "pg_connection")
