# import asyncio
from typing import Annotated, Optional

from domain.meals.events import MealInsertEvent
from taskiq import Context, TaskiqDepends


class MealsTasks:
    @staticmethod
    async def insert_meal(
        event: MealInsertEvent,
        context: Annotated[Context, TaskiqDepends()],
    ):
        repo = context.state.meals_repository

        context.broker
        # _ = self.event_class.model_validate(event_data)

        # statement, args = self.query.insert_meal(
        #     time=datetime.now(timezone.utc),
        #     meal_id=_.meal_id,
        #     user_id=_.user_id,
        #     meal_name=_.meal_name,
        #     calories=_.calories,
        # )

        # self.repository.execute(statement, args)

        print("meals repo", repo)
        return repo

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

    def __call__():
        return [
            MealsTasks.insert_meal,
            # MealsTasks.delete_meal_task,
            # MealsTasks.update_meal_task,
        ]
