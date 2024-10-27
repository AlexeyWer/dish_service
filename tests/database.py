from sqlalchemy import Table, and_, select
from sqlalchemy.ext.asyncio import AsyncConnection

from srv.store.postgres.database.base import BaseDB


class TestDB(BaseDB):
    async def check_record_exist(self, conn: AsyncConnection, table: Table, data: dict) -> int | None:
        """
        Проверить существование записи в таблице.
        """
        conditions = [
            table.columns.get(key) == value for key, value in data.items() if key in table.columns
        ]
        query = select(table.c.id).select_from(table).where(and_(*conditions)).limit(1)
        return await conn.scalar(query)