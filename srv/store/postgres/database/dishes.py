from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.base import BaseDB


class DishesDB(BaseDB):
    async def create_or_update_dish(self, conn: AsyncConnection, data: dict) -> int:
        """
        Создать/обновить рецептуры.
        """
        await self.create_or_update_record(conn, data, self.dishes)
    
    async def get_dishes(self, conn: AsyncConnection, limit: int, offset: int) -> Sequence[Row]:
        """
        Получить рецептуры.
        """
        return await self.get_records(conn, self.dishes, "name", limit, offset)