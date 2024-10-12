from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.dishes import DishesDB

class DishesService:
    db = DishesDB()

    async def create_or_update_dish(self, conn: AsyncConnection, data: dict) -> dict:
        """
        Создать/обновить продукт.
        """
        return await self.db.create_or_update_record(conn, data, self.db.dishes)
    
    async def get_dishes(self, conn: AsyncConnection, limit: int = 100, offset: int = 0) -> Sequence[Row]:
        """
        Получить продукты.
        """
        return await self.db.get_records(conn, self.db.dishes, "name", limit, offset)
    
    async def delete_dish(self, conn: AsyncConnection, record_id: int | None, column: str | None, value: Any | None) -> Sequence[Row]:
        """
        Удалить блюдо.
        """
        await self.db.delete_record(conn, self.db.dishes, record_id, column, value)

    