import logging
from typing import Dict

from asyncpg import Connection, connect

from src.adapters.spi.persistence.exceptions.database_connection_error import (
    CreateDbConnectionException,
    DatabaseQueryError,
    handle_close_connection_error,
    handle_start_connection_error,
    handle_query_error,
)
from src.adapters.spi.persistence.time_scale_db.async_mixin import AsyncMixin
from src.config.validation import FieldValidator
from src.ports.spi.persistence.repository import Repository


class TimeScaleDbRepository(FieldValidator, AsyncMixin, Repository):

    _connection: Connection
    _insert_query: str
    _delete_query: str
    _update_query: str
    connection_string: str
    database: str
    queries: Dict[str, str]

    async def __ainit__(
        self,
        connection_string: str,
        database: str,
        queries: Dict[str, str],
    ) -> None:

        await self._connect(connection_string=connection_string, database=database)

        self._insert_query = queries.get("INSERT")
        self._delete_query = queries.get("DELETE")

    @handle_start_connection_error
    async def _connect(self, connection_string: str, database: str) -> None:
        self._connection = await connect(
            dsn=connection_string,
            database=database,
        )

        logging.info(
            f"""Timescale DB connection created: 
                        ID: {id(connection_string)}
                        Connection string: {connection_string}"""
        )

    @handle_query_error
    async def insert(self, *args) -> None:
        await self._connection.execute(
            query=self._insert_query,
            *args,
        )

    @handle_query_error
    async def delete(
        self,
        *args,
    ) -> None:
        await self._connection.execute(
            query=self._delete_query,
            *args,
        )

    async def update(self, *args) -> None:
        pass

    @handle_close_connection_error
    async def close(self) -> None:
        await self._connection.close()
        logging.info(f"Closed connection {self._connection} in the pool.")
