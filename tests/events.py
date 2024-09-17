from uuid import uuid4
from src.domains.meals.events import InsertMealEvent, MealEvents
from esdbclient import (
    EventStoreDBClient,
    NewEvent,
    StreamState,
)
from faker import Faker
from pprint import pp

print("---> START EVENTS")

FAKE = Faker()
STREAM_NAME = "meals_stream"
EVENTS = 1

client = EventStoreDBClient(uri="esdb://localhost:2113?Tls=false")


def run():
    for i in range(EVENTS):
        meal = InsertMealEvent(
            user_id=uuid4(),
            meal_name=FAKE.name(),
            calories=float("{:.2f}".format(FAKE.random.uniform(10, 50))),
        )

        pp(meal.meal_name)

        event = NewEvent(
            type=MealEvents.INSERT.value,
            data=bytes(meal.model_dump_json(), encoding="utf-8"),
        )

        # printer(f"EVENT:\n{event}\n")

        client.append_to_stream(
            stream_name=STREAM_NAME,
            current_version=StreamState.ANY,
            events=event,
        )

    print("---> END EVENTS")


if __name__ == "__main__":
    run()
