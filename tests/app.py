from aiohttp.test_utils import TestClient

from srv.web.context import Context

from tests.database import TestDB


class TestApp:
    db = TestDB()

    def __init__(self, client: TestClient):
        self.client = client
        self.ctx: Context = getattr(client.app, "context")
    
    async def __aenter__(self) -> "TestApp":
        self.conn = await self.ctx.postgres_accessor.engine.connect()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.rollback()
        await self.conn.close()