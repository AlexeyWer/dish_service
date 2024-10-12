from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.products_in_dishes import ProductsInDishesDB

class ProductsInDishesService:
    db = ProductsInDishesDB()

    async def add_product_in_dish(self, conn: AsyncConnection, data: dict) -> dict:
        """
        Добавить продукт в блюдо.
        """
        return await self.db.create_or_update_record(conn, data, self.db.products_in_dishes)
    
    async def get_products_in_dishes(self, conn: AsyncConnection, dish_name: str) -> Sequence[Row]:
        """
        Получить продукты в блюде.
        """
        return await self.db.get_products_in_dishes(conn, dish_name)

    async def delete_product_in_dish(self, conn: AsyncConnection, record_id: int) -> None:
        """
        Удалить продукт из блюда.
        """
        await self.db.delete_record(conn, self.db.products_in_dishes, record_id=record_id)
