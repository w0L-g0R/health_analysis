from asyncpg import Pool

from src.database.time_scale_db.exceptions.database_connection_error import (
    handle_query_error,
)
from src.config.field_validator import FieldValidator
from src.interfaces.queries import Queries
from src.interfaces.repository import Repository


class MealsRepository(FieldValidator, Repository):

    connection_pool: Pool
    queries: Queries

    @handle_query_error
    async def add(self, args):
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
