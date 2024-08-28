from uuid import uuid4

from esdbclient import (
    EventStoreDBClient,
    NewEvent,
    StreamState,
)
from faker import Faker

from api.meals.models import Meal

print("---> START EVENTS")

FAKE = Faker()
STREAM_NAME = "stream_one"
EVENTS = 1

client = EventStoreDBClient(uri="esdb://localhost:2113?Tls=false")


def run():
    for i in range(EVENTS):
        meal = Meal(
            meal_id=uuid4(),
            user_id=uuid4(),
            meal_name=FAKE.name(),
            calories="{:.2f}".format(FAKE.random.uniform(10, 50)),
        )

        # printer(f"MEAL:\n{meal}\n")

        event = NewEvent(
            type="InsertMeal",
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
