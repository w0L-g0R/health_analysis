# import asyncio
from typing import Annotated, Optional

from taskiq import Context, TaskiqDepends


class MealsTasks:
    async def insert_meal(
        event: str,
        context: Annotated[Context, TaskiqDepends()],
    ) -> Optional[str]:
        repo = context.state.meals_repository

        print("meals repo", repo)
        return repo

    async def update_meal_task(
        context: Annotated[Context, TaskiqDepends()],
    ) -> Optional[str]:
        c = context.state.client

        print("context.client", c)
        return c

    async def delete_meal_task(
        context: Annotated[Context, TaskiqDepends()],
    ) -> Optional[str]:
        c = context.state.client

        print("context.client", c)
        return c

    def __call__():
        return [
            MealsTasks.insert_meal,
            MealsTasks.delete_meal_task,
            MealsTasks.update_meal_task,
        ]
