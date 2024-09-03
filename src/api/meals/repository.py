import logging

from asyncpg import Pool


class MealsRepository:
    def __init__(self, pool: Pool):
        self.pool = pool
        if pool:
            logging.info(
                f"Initialized meals repository {id(self)} with pool {id(self.pool)}",
            )

    async def execute(self, statement: str, args: tuple):
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(statement, *args)

        except Exception as e:
            logging.error(e)

    async def close(self):
        if self.pool:
            await self.pool.close()
            logging.info(
                f"Closed meals repository {id(self)} with pool {id(self.pool)}: {self.pool._closed}",
            )
