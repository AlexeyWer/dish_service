from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.base import BaseDB


class ProductsInDishesDB(BaseDB):
    async def add_product_in_dish(self, conn: AsyncConnection, data: dict) -> int:
        """
        Создать/обновить продукт.
        """
        await self.create_or_update_record(conn, data, self.products)
    
    async def get_products(self, conn: AsyncConnection, limit: int, offset: int) -> Sequence[Row]:
        """
        Получить продукты.
        """
        return await self.get_records(conn, self.products, "name", limit, offset)
