from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.products import ProductsDB

class ProductsService:
    db = ProductsDB()

    async def create_or_update_product(self, conn: AsyncConnection, data: dict) -> None:
        """
        Создать/обновить продукт.
        """
        await self.db.create_or_update_product(conn, data)
    
    async def get_products(self, conn: AsyncConnection, limit: int = 100, offset: int = 0) -> Sequence[Row]:
        """
        Получить продукты.
        """
        return await self.db.get_products(conn, limit, offset)

    async def delete_product(self, conn: AsyncConnection, pk: int | None, column: str | None, value: Any | None) -> Sequence[Row]:
        """
        Получить продукты.
        """
        await self.db.delete_product(conn, pk, column, value)
