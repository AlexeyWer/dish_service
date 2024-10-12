import logging
from typing import Any, Sequence

from sqlalchemy import Table, UniqueConstraint, select, bindparam, delete
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.engine.row import Row

from srv.store.postgres.tables import Tables


logger = logging.getLogger(__name__)


class BaseDB(Tables):
    
    async def create_or_update_record(self, conn: AsyncConnection, data: dict, table: Table) -> dict:
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
            .returning(table)
        )
        resp = await conn.execute(statement=query, parameters=data)
        return resp.mappings().fetchone()
    
    async def get_records(
        self,
        conn: AsyncConnection,
        table: Table,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[Row]:
        """
        Получить записи из таблицы.
        """
        query = select(table).select_from(table).limit(limit).offset(offset)
        if order_by:
            query.order_by(table.columns.get(order_by))
        if limit:
            query.limit(limit)
        if offset:
            query.order_by(offset)
        resp = await conn.execute(query)
        return resp.fetchall()

    async def delete_record(
        self, conn: AsyncConnection,
        table: Table,
        record_id: int | None,
        column: str | None,
        value: Any | None,
    ) -> None:
        """
        Удалить запись из таблицы.
        """
        if id:
            condition = table.c.id == record_id
        elif column and value and column in table.columns:
            condition = table.columns.get(column) == value
        else:
            return
        query = delete(table).where(condition)
        await conn.execute(query)