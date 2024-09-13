# import asyncio
import asyncio
from typing import Annotated, Optional

from dependencies.database import DB
from domain.meals.events import MealInsertEvent
from taskiq import Context, TaskiqDepends


class MealsTasks:
    @staticmethod
    async def insert_meal(
        event: str,
        database: Annotated[DB, TaskiqDepends()],
        context: Annotated[Context, TaskiqDepends()],
    ) -> str:
        # repo = context.state.meals_repository

        # context.state.database
        print("context: ", context.state)
        print("database.id: ", database.id)
        await asyncio.sleep(5)

        # context.broker
        # _ = self.event_class.model_validate(event_data)

        # statement, args = self.query.insert_meal(
        #     time=datetime.now(timezone.utc),
        #     meal_id=_.meal_id,
        #     user_id=_.user_id,
        #     meal_name=_.meal_name,
        #     calories=_.calories,
        # )

        # self.repository.execute(statement, args)

        print("meals event", event)
        return event

    # async def update_meal_task(
    #     context: Annotated[Context, TaskiqDepends()],
    # ) -> Optional[str]:
    #     c = context.state.client

    #     print("context.client", c)
    #     return c

    # async def delete_meal_task(
    #     context: Annotated[Context, TaskiqDepends()],
    # ) -> Optional[str]:
    #     c = context.state.client

    #     print("context.client", c)
    #     return c
