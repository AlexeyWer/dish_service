import logging

from argparse import Namespace
from aiohttp.web import Application, run_app

from srv.web.context import Context
from srv.web.middleware import Middleware
from srv.web.routes import Routes


logger = logging.getLogger(__name__)


class Server:
    def __init__(self, args: Namespace | None = None):
        self.args = args
        self.app = Application(client_max_size=200 * 1024 ** 2)
        self.ctx = Context(self.app)
        setattr(self.app, "context", self.ctx)

    def make_app(self) -> None:
        """
        Настроить сервер.
        """
        Middleware(self.app)
        Routes(self.app)

    def start_server(self) -> None:
        """
        Запустить сервер.
        """
        self.make_app()
        logger.info(f"Starting app on {self.ctx.config.host}:{self.ctx.config.port}")
        run_app(self.app, host=self.ctx.config.host, port=self.ctx.config.port)
