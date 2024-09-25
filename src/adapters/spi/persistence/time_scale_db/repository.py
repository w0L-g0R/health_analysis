import logging
from asyncpg import connect

from src.adapters.spi.persistence.time_scale_db.async_mixin import AsyncMixin
from src.ports.spi.persistence.repository import Repository


class TimeScaleDbRepository(AsyncMixin, Repository):

    async def __ainit__(
        self,
        user: str,
        password: str,
        database: str,
        host: str,
        port: str,
        queries: dict[str, str],
    ) -> None:
        await self._connect(database, host, password, port, user)

        self._insert_query = queries.get("INSERT")
        self._delete_query = queries.get("DELETE")

    async def _connect(self, database, host, password, port, user):
        try:
            self.connection = await connect(
                user=user,
                password=password,
                database=database,
                host=host,
                port=port,
            )

            logging.info(f"Timescale DB connection created: {id(self.connection)}")

        except Exception as e:
            logging.error(f"Error initializing connection: {e}")
            raise

    async def insert(self, *args) -> None:
        try:
            if self.connection:
                await self.connection.execute(
                    self._insert_query,
                    *args,
                )

        except Exception:
            logging.error(
                f"Error executing: {self._insert_query} with args {list(*args)}"
            )
            raise

    async def delete(
        self,
        *args,
    ) -> None:
        try:
            if self.connection:
                await self.connection.execute(
                    self._delete_query,
                    *args,
                )

        except Exception:
            logging.error(
                f"Error executing: {self._delete_query} with args {list(*args)}"
            )
            raise

    async def update(self, *args) -> None:
        pass

    async def close(self) -> None:
        if self.connection:
            try:
                await self.connection.close()
                logging.info(f"Closed connection {self.connection} in the pool.")

            except Exception as e:
                logging.error(f"Error closing connection {self.connection}: {e}")
                raise
