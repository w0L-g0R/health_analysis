from pprint import pp
from uuid import uuid4

from esdbclient import EventStoreDBClient, NewEvent, StreamState
from faker import Faker

from src.events.meals.add_meal_event import AddMealEvent

print("---> START EVENTS")

FAKE = Faker()
STREAM_NAME = "StreamMeals"
EVENTS = 1

client = EventStoreDBClient(uri="esdb://localhost:2113?Tls=false")


def run():
    for i in range(EVENTS):
        meal = AddMealEvent(
            meal_id=uuid4(),
            user_id=uuid4(),
            meal_name=FAKE.name(),
            calories=float("{:.2f}".format(FAKE.random.uniform(10, 50))),
        )

        pp(meal.meal_name)

        event = NewEvent(
            type=AddMealEvent.__name__,
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
