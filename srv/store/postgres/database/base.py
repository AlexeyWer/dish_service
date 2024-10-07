import logging
from typing import Any, Sequence

from sqlalchemy import Column, Table, UniqueConstraint, select, update, bindparam, delete
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.engine.row import Row

from srv.store.postgres.tables import Tables


logger = logging.getLogger(__name__)


class BaseDB(Tables):
    
    async def create_or_update_record(self, conn: AsyncConnection, data: dict, table: Table) -> int:
        """
        Создать/обновить запись в таблице.
        """
        bind_data = {key: bindparam(key) for key in data if key in table.columns}
        unique_columns_names = set()
        for constrain in table.constraints:
            if isinstance(constrain, UniqueConstraint):
                [unique_columns_names.add(column) for column in constrain.columns]
        query = (
            psql.insert(table)
            .values(bind_data)
            .on_conflict_do_update(index_elements=unique_columns_names, set_=bind_data)
        )
        await conn.execute(statement=query, parameters=data)
    
    async def get_records(
        self, conn: AsyncConnection, table: Table, order_by: str, limit: int, offset: int
    ) -> Sequence[Row]:
        """
        Получить записи из таблицы.
        """
        query = select(table).select_from(table).limit(limit).offset(offset)
        if order_by:
            quit.order_by(table.columns.get(order_by))
        resp = await conn.execute(query)
        return resp.fetchall()

    async def delete_record(
        self, conn: AsyncConnection,
        table: Table,
        pk: int | None,
        column: str | None,
        value: Any | None,
    ) -> None:
        """
        Удалить запись из таблицы.
        """
        if pk:
            condition = table.c.id == pk
        elif column and value and column in table.columns:
            condition = table.columns.get(column) == value
        else:
            return
        query = delete(table).where(condition)
        await conn.execute(query)