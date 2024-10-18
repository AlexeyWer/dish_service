import logging
from typing import Awaitable, Callable
from http import HTTPStatus

from aiohttp_apispec import validation_middleware
from aiohttp.web import Application, Request, Response, middleware, HTTPException

from srv.web.context import Context


HanderT = Callable[[Request], Awaitable[Response]]


logger = logging.getLogger(__name__)


class Middleware:

    def __init__(self, app: Application):
        self.app = app
        self.ctx: Context = getattr(self.app, "context")
        self.__add_middlewares()
    
    @middleware
    async def __catch_exceptions(self, request: Request, handler: HanderT) -> Response:
        """
        Отловить исключения.
        """
        try:
            return await handler(request)
        except HTTPException:
            raise
        except Exception as exc:
            logger.error(f"Не обработанная ошибка:\n{exc}", exc_info=True)
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, text="Server error")
    
    @middleware
    async def __create_postgres_connection(self, request: Request, handler: HanderT) -> Response:
        """
        Создать подключение к postgres в зависимости от типа запроса.
        """
        if request.method in ("GET", "HEAD", "OPTION"):
            create_connect = self.ctx.postgres_accessor.engine.connect
        else:
            create_connect = self.ctx.postgres_accessor.engine.begin
        
        async with create_connect() as conn:
            setattr(request, "pg_connection", conn)
            return await handler(request)
        

    def __add_middlewares(self) -> None:
        """
        Подключить промежуточное ПО к серверу.
        """
        self.app.middlewares.append(self.__catch_exceptions)
        self.app.middlewares.append(validation_middleware)
        self.app.middlewares.append(self.__create_postgres_connection)
