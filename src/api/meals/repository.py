import logging

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Dependency,
    Singleton,
)
from psycopg2.pool import SimpleConnectionPool


class MealsRepository:
    def __init__(self, pool: SimpleConnectionPool):
        self.pool = pool
        if pool:
            logging.info(
                f"Initialized meals repository {id(self)} with pool {id(self.pool)}",
            )

    # def insert():
    #     INSERT_MEAL

    def close(self):
        if self.pool:
            self.pool.closeall()
            logging.info(
                f"Closed meals repository {id(self)} with pool {id(self.pool)}: {self.pool.closed}",
            )


class Meals(DeclarativeContainer):
    pool = Dependency(instance_of=SimpleConnectionPool)

    repository = Singleton(MealsRepository, pool=pool)
