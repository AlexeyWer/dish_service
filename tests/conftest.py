import logging
import os
from contextlib import asynccontextmanager

import pytest_asyncio
from aiohttp.test_utils import TestClient
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from testcontainers.postgres import PostgresContainer
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.ext.asyncio import AsyncConnection

from srv.web.app import Server

from tests.app import TestApp


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_db():
    postgres_container = PostgresContainer("postgres:13-alpine", dbname="test_dishes")
    postgres_container.start()
    logger.info("Создан docker контейнер с базой postgres")

    alembic_ini = os.path.join(BASE_DIR, "alembic.ini")
    if database_exists(postgres_container.get_connection_url()):
        drop_database(postgres_container.get_connection_url())
    create_database(postgres_container.get_connection_url())
    alembic_config = AlembicConfig(alembic_ini)
    alembic_command.upgrade(alembic_config, "head")
    logger.info("Миграции успешно выполнены")

    os.environ.update(
        {
            "POSTGRES_HOST": postgres_container.get_container_host_ip(),
            "POSTGRES_PORT": postgres_container.get_exposed_port(port=5432),
            "POSTGRES_DB_NAME": postgres_container.dbname,
            "POSTGRES_USERNAME": postgres_container.username,
            "POSTGRES_PASSWORD": postgres_container.password,
        }
    )
    logger.info("Обновлены переменные окружения")
    yield
    postgres_container.stop()


@pytest_asyncio.fixture
async def make_test_client(aiohttp_client):
    srv = Server()
    srv.make_app()
    client: TestClient = await aiohttp_client(srv.app)
    yield client
    await srv.app.cleanup()
    await client.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_app(make_test_client: TestClient, mocker):
    async with TestApp(make_test_client) as test_app:
        @asynccontextmanager
        async def get_conn():
            yield test_app.conn
        mocker.patch("sqlalchemy.ext.asyncio.AsyncEngine.connect", side_effect=get_conn)
        mocker.patch("sqlalchemy.ext.asyncio.AsyncEngine.begin", side_effect=get_conn)
        yield test_app