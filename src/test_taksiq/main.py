# import asyncio
import asyncio

from meals_broker import meals_broker
from meals_tasks import MealsTasks


async def main() -> None:
    await meals_broker.startup()

    insert_meal_task = meals_broker.find_task(
        task_name=MealsTasks.insert_meal.__name__
    )

    print("insert_meal_task:", insert_meal_task)

    insert_meal_task = await insert_meal_task.kiq(
        "insert_meal_event"
    )

    insert_meal_task_result = (
        await insert_meal_task.wait_result()
    )

    print(
        f"Got client value: {insert_meal_task_result.is_err}"
    )

    await meals_broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
