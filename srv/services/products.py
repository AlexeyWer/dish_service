from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.products import ProductsDB

class ProductsService:
    db = ProductsDB()

    async def create_or_update_product(self, conn: AsyncConnection, data: dict) -> dict:
        """
        Создать/обновить продукт.
        """
        return await self.db.create_or_update_record(conn, data, self.db.products)
    
    async def get_products(self, conn: AsyncConnection, limit: int = 100, offset: int = 0) -> Sequence[Row]:
        """
        Получить продукты.
        """
        return await self.db.get_records(conn, self.db.products, "name", limit, offset)

    async def delete_product(self, conn: AsyncConnection, record_id: int | None, column: str | None, value: Any | None) -> Sequence[Row]:
        """
        Получить продукты.
        """
        await self.db.delete_record(conn, self.db.products, record_id, column, value)
