from asyncpg import Connection
from pydantic import PrivateAttr

from src.adapters.spi.persistence.exceptions.database_connection_error import (
    handle_query_error,
)
from src.config.field_validator import FieldValidator
from src._LEGACY.meal_repository import Repository
from src.ports.api.use_cases.meals.remove_meal.remove_meal_use_case import (
    RemoveMealUseCase,
)
from src.ports.spi.persistence.create_meal_port import CreateMealPort


class MealsRepository(FieldValidator, CreateMealPort, RemoveMealUseCase):

    _connection: Connection = PrivateAttr()

    @handle_query_error
    async def create_meal(self, *args) -> None:

        query = """
                INSERT INTO meals (time, meal_id, user_id, meal_name, calories) VALUES ($1, $2, $3, $4, $5)
         """

        await self._connection.execute(
            query=query,
            *args,
        )

    @handle_query_error
    async def delete_meal(
        self,
        *args,
    ) -> None:

        query = """
            DELETE FROM meals WHERE meal_id = $1 AND user_id = $2
        """

        await self._connection.execute(
            query=query,
            *args,
        )

    async def update(self, query: str, *args) -> None:
        pass
