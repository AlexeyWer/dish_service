from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.engine.row import Row

from srv.store.postgres.database.base import BaseDB


class ProductsDB(BaseDB):
    ...
