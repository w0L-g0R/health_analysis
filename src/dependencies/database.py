import logging
from typing import Optional
from uuid import uuid4

from asyncpg import create_pool
from asyncpg.pool import Pool


async def init_async_timescale_db_pool(config: dict) -> Pool:
    try:
        pool = await create_pool(
            user=config["user"],
            password=config["password"],
            database=config["database"],
            host=config["host"],
            port=config["port"],
        )

        logging.info(f"Timescale DB pool created: {id(pool)}")
        if pool:
            return pool

    except Exception as e:
        logging.error(f"Error initializing connection pool: {e}")
        raise


class DB:
    id = uuid4()

    @classmethod
    def exec(cls):
        print("Executing in DB:", cls.id)

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
