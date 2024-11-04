from typing import Sequence

from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.base import BaseDB


class ProductsInDishesDB(BaseDB):
    async def get_products_in_dishes(self, conn: AsyncConnection, dish_id: int) -> Sequence[Row]:
        """
        Получить продукты в блюде.
        """
        resp = await conn.execute(
            select(
                self.products_in_dishes.c.id,
                self.products.c.name,
                self.products_in_dishes.c.quantity,
                self.products.c.measure,
            )
            .select_from(self.dishes)
            .join(self.products_in_dishes, self.products_in_dishes.c.dish == self.dishes.c.id)
            .join(self.products, self.products.c.id == self.products_in_dishes.c.product)
            .where(self.dishes.c.id == dish_id)
            .order_by(self.products_in_dishes.c.id)
        )
        return resp.fetchall()

    async def delete_product_in_dish(self, conn: AsyncConnection, dish_id: int, record_id: int) -> None:
        """
        Удалить продукт из блюда.
        """
        await conn.execute(
            delete(self.products_in_dishes)
            .where(
                and_(
                    self.products_in_dishes.c.dish == dish_id,
                    self.products_in_dishes.c.id == record_id,
                )
            )
        )
