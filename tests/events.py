from pprint import pp
from uuid import uuid4

from esdbclient import EventStoreDBClient, NewEvent, StreamState
from faker import Faker

from src.ports.api.use_cases.meals.add_meal.add_meal_dto import AddMealDto

print("---> START EVENTS")

FAKE = Faker()
STREAM_NAME = "meals_stream"
EVENTS = 1

client = EventStoreDBClient(uri="esdb://localhost:2113?Tls=false")


def run():
    for i in range(EVENTS):
        meal = AddMealDto(
            user_id=uuid4(),
            meal_name=FAKE.name(),
            calories=float("{:.2f}".format(FAKE.random.uniform(10, 50))),
        )

        pp(meal.meal_name)

        event = NewEvent(
            type=AddMealDto.__name__,
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
