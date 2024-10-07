import aiohttp_cors
from aiohttp.web import Application

from srv.api.v1.routes import v1_routes
from srv.web.context import Context


class Routes:

    def __init__(self, app: Application):
        self.app = app
        self.ctx: Context = getattr(self.app, "context")
        self.__create_routes()
    
    def __get_cors(self) -> aiohttp_cors.CorsConfig:
        return aiohttp_cors.setup(
            self.app,
            defaults={
                "*", aiohttp_cors.ResourceOptions(
                    allow_credentials=True, expose_headers="*", allow_headers="*"
                )
            }
        )
    
    def __create_routes(self) -> None:
        """
        Настроить роуты.
        """
        v1_routes(self.app, self.ctx)