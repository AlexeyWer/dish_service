import logging
import os
from contextlib import asynccontextmanager

import pytest_asyncio
from aiohttp.test_utils import TestClient
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from testcontainers.postgres import PostgresContainer
from sqlalchemy_utils import create_database, database_exists, drop_database

from srv.web.app import Server

from tests.accesor import TestAccessor


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_db():
    sync_url = (
        f"postgresql://{os.environ.get("POSTGRES_USERNAME")}:{os.environ.get("POSTGRES_PASSWORD")}@"
        f"{os.environ.get("POSTGRES_HOST")}:{os.environ.get("POSTGRES_PORT")}/{os.environ.get("POSTGRES_DB_NAME")}"
    )
    alembic_ini = os.path.join(BASE_DIR, "alembic.ini")
    if database_exists(sync_url):
        drop_database(sync_url)
    create_database(sync_url)
    alembic_config = AlembicConfig(alembic_ini)
    alembic_command.upgrade(alembic_config, "head")
    logger.info("Миграции успешно выполнены")
    yield


@pytest_asyncio.fixture
async def make_test_client(aiohttp_client):
    srv = Server()
    srv.make_app()
    client: TestClient = await aiohttp_client(srv.app)
    yield client
    await srv.app.cleanup()
    await client.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_accessor(make_test_client: TestClient, mocker):
    async with TestAccessor(make_test_client) as accessor:
        @asynccontextmanager
        async def get_conn():
            yield accessor.conn
        mocker.patch("sqlalchemy.ext.asyncio.AsyncEngine.connect", side_effect=get_conn)
        mocker.patch("sqlalchemy.ext.asyncio.AsyncEngine.begin", side_effect=get_conn)
        yield accessor
