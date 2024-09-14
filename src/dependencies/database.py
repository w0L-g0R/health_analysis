import logging

import asyncpg


async def init_async_timescale_db_connection(config: dict):
    try:
        connection = await asyncpg.connect(
            user=config["user"],
            password=config["password"],
            database=config["database"],
            host=config["host"],
            port=config["port"],
        )

        logging.info(
            f"Timescale DB connection created: {id(connection)}"
        )
        return connection

    except Exception as e:
        logging.error(f"Error initializing connection: {e}")
        raise


class TimeScaleDatabase:
    def __init__(self, connection):
        self.connection = connection

    async def execute(self, statement, args):
        try:
            await self.connection.execute(statement, args)
        except Exception:
            logging.error(
                f"Error executing: {statement} with args {args}"
            )
            raise

    def close(self):
        if self.connection:
            try:
                logging.info(
                    f"Closing connection {self.connection} in the pool."
                )
                self.connection.close()
            except Exception:
                logging.error(
                    f"Error closing connection {self.connection}"
                )
                raise
