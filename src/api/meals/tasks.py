import dramatiq
from psycopg2.sql import SQL

from api.clients.timescale import TimescaleDbClient
from api.meals.types import InsertMealArgs
from config import MEALS_QUEUE, TIMESCALE_DB

client = TimescaleDbClient(connection=TIMESCALE_DB)


class MealTasks:
    @dramatiq.actor(queue_name=MEALS_QUEUE)
    @staticmethod
    def execute_insert_meal(
        statement: SQL,
        args: InsertMealArgs,
    ) -> None:
        client.execute(statement, args)
