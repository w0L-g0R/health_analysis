import json
from traceback import print_tb
from uuid import uuid4

import psycopg2
from asyncpg import Connection, Pool
from pydantic import PrivateAttr
from redis import ConnectionPool

from src.adapters.spi.persistence.time_scale_db.exceptions.database_connection_error import (
    handle_query_error,
)
from src.config.field_validator import FieldValidator
from src.ports.spi.queries import Queries
from src.ports.spi.repository import Repository


class MealsRepository(FieldValidator, Repository):

    connection_pool: Pool
    queries: Queries

    @handle_query_error
    async def add(self, args):
        print("args", *args)
        a = args
        print("a", a)
        # c = uuid4()
        # d = uuid4()
        # e = json.dumps({"calories": 100, "meal_name": "test"})
        # a = tuple([c, d, e])
        try:
            await self.connection_pool.execute(
                """
                    INSERT INTO meals (meal_id, user_id, meal_data)
                    VALUES ($1, $2, $3)
                """,
                *args,
            )
        except Exception as error:
            print(error)
        # r = await self.connection_pool.fetch("SELECT * FROM meals")
        # print(r)

    # return await self.connection_pool.execute(
    #     query=self.queries.add(),
    #     *args,
    # )

    @handle_query_error
    async def delete(
        self,
        *args,
    ) -> None:

        await self.connection_pool.execute(
            query=self.queries.add(),
            *args,
        )

    async def update(self, *args) -> None:
        pass
