import logging

import sentry_sdk 
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp.web import Application
from sentry_sdk.integrations import aiohttp as aiohttp_sdk
from sentry_sdk.integrations import logging as logging_sdk

from srv.settings.configs import ServerConfig
from srv.store.postgres.accessor import PostgresAccessor


class Context:
    config = ServerConfig()
    postgres_accessor = PostgresAccessor()
    
    def __init__(self, app: Application):
        self.app = app
        self.__init_ctx()

    
    def __init_ctx(self) -> None:
        """
        Инициализировать настройки сервера.
        """
        self.__configure_logger()
        self.__init_sentry()
        self.__init_docs()
        self.app.cleanup_ctx.append(self.postgres_accessor.lifespan_connections)

    def __configure_logger(self)  -> None:
        """
        Сконфигурировать логгер.
        """
        logging.basicConfig(level=self.config.logging_level, format=self.config.logging_format)

    def __init_sentry(self) -> None:
        """
        Подключение Sentry.
        """
        sentry_sdk.init(
            dsn=self.config.sentry_dsn,
            integrations=[
                aiohttp_sdk.AioHttpIntegration(),
                logging_sdk.LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
            ],
            server_name=self.config.name,
            release=self.config.release,
        )
    
    def __init_docs(self) -> None:
        """
        Подключение документации.
        """
        setup_aiohttp_apispec(
            app=self.app,
            title=self.config.name,
            version=self.config.release,
            url=f"/{self.config.name}/docs/swagger.json",
            swagger_path=f"/{self.config.name}/docs",
            static_path=f"/{self.config.name}/static/swagger"
        )
