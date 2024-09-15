import logging

from asyncpg import connect
from shared.async_mixin import AsyncMixin


class TimeScaleDatabase(AsyncMixin):
    async def __ainit__(self, config: dict):
        try:
            self.connection = await connect(
                user=config["user"],
                password=config["password"],
                database=config["database"],
                host=config["host"],
                port=config["port"],
            )

            logging.info(
                f"Timescale DB connection created: {id(self.connection)}"
            )

        except Exception as e:
            logging.error(
                f"Error initializing connection: {e}"
            )
            raise

    async def execute(self, statement, args):
        try:
            if self.connection:
                await self.connection.execute(
                    statement, *args
                )
        except Exception:
            logging.error(
                f"Error executing: {statement} with args {args}"
            )
            raise

    async def close(self):
        if self.connection:
            try:
                await self.connection.close()
                logging.info(
                    f"Closed connection {self.connection} in the pool."
                )
            except Exception as e:
                logging.error(
                    f"Error closing connection {self.connection}: {e}"
                )
                raise
