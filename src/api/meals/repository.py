from dataclasses import dataclass
import logging

from asyncpg import Pool


# from psycopg2.errors.
@dataclass
class MealsMutations:
    insert_statement = """ INSERT INTO meals (data) VALUES ($1);"""


class MealsRepository:
    def __init__(self, pool: Pool):
        self.pool = pool
        if pool:
            logging.info(
                f"Initialized meals repository {id(self)} with pool {id(self.pool)}",
            )

    async def execute(self, statement, data):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(statement, data)

        # except DataBaseError as e:
        #     logging.error(e)

        except Exception as e:
            logging.error(e)

        finally:
            await connection.close()

    def close(self):
        if self.pool:
            self.pool.close()
            logging.info(
                f"Closed meals repository {id(self)} with pool {id(self.pool)}: {self.pool.closed}",
            )
