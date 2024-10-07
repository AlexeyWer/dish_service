from typing import Any, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.base import BaseDB


class ProductsDB(BaseDB):
    async def create_or_update_product(self, conn: AsyncConnection, data: dict) -> int:
        """
        Создать/обновить продукт.
        """
        await self.create_or_update_record(conn, data, self.products)
    
    async def get_products(self, conn: AsyncConnection, limit: int, offset: int) -> Sequence[Row]:
        """
        Получить продукты.
        """
        return await self.get_records(conn, self.products, "name", limit, offset)

    async def delete_product(self, conn: AsyncConnection, pk: int | None = None, column: str | None = None, value: Any | None = None) -> None:
        """
        Удалить продукт.
        """
        await self.delete_record(conn, self.products, pk, column, value)

