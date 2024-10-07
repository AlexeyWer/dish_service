import asyncio
import logging
from typing import AsyncGenerator

from aiohttp.web import Application
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from srv.settings.configs import PostgresConfig
from srv.store.abc.db_accessor import BaseDBAccessor


logger = logging.getLogger(__name__)


class PostgresAccessor(BaseDBAccessor):
    __config = PostgresConfig()
    __engine: AsyncEngine

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine
    
    async def lifespan_connections(self, app: Application) -> AsyncGenerator:
        """
        Создать пул соединений с postgres.
        """
        async with asyncio.timeout(10):
            self.__engine = create_async_engine(
                f"postgresql+asyncpg://{self.__config.username}:{self.__config.password}"
                f"@{self.__config.host}:{self.__config.port}/{self.__config.db_name}",
                echo=False,
                pool_size=self.__config.pool_size,
                max_overflow=self.__config.max_overflow,
                query_cache_size=50,
                pool_timeout=30,
                pool_pre_ping=True,
            )
            if not await self.ping():
                raise ConnectionError("Failed to connect to postgres")
            logger.info(f"Create connection pool for postgres, db_name: {self.__config.db_name}")
        yield
        await self.__engine.dispose()
    
    async def ping(self) -> bool:
        """
        Проверить соединение с postgres.
        """
        async with self.engine.connect() as conn:
            if await conn.execute(text("SELECT 1")):
                return True
            return False
