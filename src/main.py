import asyncio

from esdbclient import EventStoreDBClient

from api.meals.handler import MealsEventHandler
from api.meals.models import Meal
from api.meals.mutations import MealMutations
from api.meals.tasks import MealTasks
from config import EVENTSTORE


async def event_listener():
    esdb_client = EventStoreDBClient(uri=EVENTSTORE)
    meals_subscription = esdb_client.subscribe_to_stream(
        stream_name="stream_one", from_end=True
    )

    while True:
        for i, event in enumerate(meals_subscription):
            data = event.data.decode("utf-8")
            meal = Meal.model_validate_json(data)
            print("type: ", event.type)

            if event.type == "InsertMeal":
                MealsEventHandler.handle_insert_event()
                statement, args = MealMutations.insert_meal(
                    meal=meal
                )

                MealTasks.insert_meal.send(
                    statement=statement,
                    args=args,
                )

                await asyncio.sleep(0.1)

        print("-----------------------------> Committed \n")


def run():
    print("Started data store event listener")
    asyncio.run(event_listener())


if __name__ == "__main__":
    run()
