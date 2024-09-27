import logging
from typing import Optional

from asyncpg import Connection, connect
from dependency_injector.resources import AsyncResource, T
from pydantic import Field, PrivateAttr

from src.adapters.spi.persistence.exceptions.database_connection_error import (
    handle_close_connection_error,
    handle_start_connection_error,
    handle_query_error,
)
from src.config.field_validator import FieldValidator
from src.ports.spi.persistence.repository import Repository


class TimeScaleDbRepository(FieldValidator, Repository):

    _connection: Connection = PrivateAttr()

    def __init__(self, connection: Connection):
        super().__init__()
        self._connection = connection

    @handle_query_error
    async def insert(self, query_insert: str, *args) -> None:
        await self._connection.execute(
            query=query_insert,
            *args,
        )

    @handle_query_error
    async def delete(
        self,
        query_delete: str,
        *args,
    ) -> None:
        await self._connection.execute(
            query=self.query_delete,
            *args,
        )

    async def update(self, query: str, *args) -> None:
        pass
