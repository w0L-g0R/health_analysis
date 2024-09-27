from asyncpg import Connection, Pool
from pydantic import PrivateAttr
from redis import ConnectionPool

from src.adapters.spi.persistence.time_scale_db.exceptions.database_connection_error import (
    handle_query_error,
)
from src.config.field_validator import FieldValidator
from src.ports.spi.queries import Queries
from src.ports.spi.repository import Repository


class MealsRepository(FieldValidator, Repository):

    connection_pool: Pool
    queries: Queries

    @handle_query_error
    async def add(self, *args) -> None:

        await self.connection_pool.execute(
            query=self.queries.add(),
            *args,
        )

    @handle_query_error
    async def delete(
        self,
        *args,
    ) -> None:

        await self.connection_pool.execute(
            query=self.queries.add(),
            *args,
        )

    async def update(self, *args) -> None:
        pass
