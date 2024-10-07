from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.dishes import DishesDB

class DishesService:
    db = DishesDB()

    async def create_or_update_dish(self, conn: AsyncConnection, data: dict) -> None:
        """
        Создать/обновить продукт.
        """
        await self.db.create_or_update_dish(conn, data)
    
    async def get_dishes(self, conn: AsyncConnection, limit: int = 100, offset: int = 0) -> Sequence[Row]:
        """
        Получить продукты.
        """
        return await self.db.get_dishes(conn, limit, offset)

