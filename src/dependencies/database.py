import logging
from typing import Optional

from asyncpg import create_pool
from asyncpg.pool import Pool


async def init_async_timescale_db_pool(config: dict) -> Optional[Pool]:
    try:
        pool = await create_pool(
            user=config["user"],
            password=config["password"],
            database=config["database"],
            host=config["host"],
            port=config["port"],
        )

        logging.info(f"Timescale DB pool created: {id(pool)}")
        return pool

    except Exception as e:
        logging.error(f"Error initializing connection pool: {e}")
        raise


class DB:
    def exec(self):
        print("Executing in DB")

    pass


class TimeScaleDatabase:
    def __init__(self, pool):
        self.pool = pool

    def execute(self, statement, data):
        connection = None
        try:
            connection = self.pool.getconn()
            cursor = connection.cursor()
            cursor.execute(statement, data)
            connection.commit()
            cursor.close()

        except Exception as e:
            if connection:
                connection.rollback()
            logging.error(f"Error executing query: {e}")

        finally:
            if connection:
                self.pool.putconn(connection)

    def close(self):
        if self.pool:
            self.pool.closeall()
            logging.info("Closed all connections in the pool.")
