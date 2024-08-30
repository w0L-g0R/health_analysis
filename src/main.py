from pprint import pprint

from dependency_injector.wiring import Provide, inject
from psycopg2.pool import SimpleConnectionPool

from config import CONFIG
from container.app import AppContainer


@inject
def main(
    timescale_db_pool: SimpleConnectionPool = Provide[
        AppContainer.pools.timescale_db_pool
    ],
) -> None:
    pool = next(timescale_db_pool)
    print("pool: ", pool)

    conn = pool.getconn()
    print("conn: ", conn)


def start():
    print("\nStart IOC container setup with config:\n")
    pprint(
        CONFIG,
        indent=2,
    )

    app = AppContainer(config=CONFIG)
    app.init_resources()
    app.wire(modules=[__name__])
    app.check_dependencies()

    main()
    # asyncio.run(event_listener())


if __name__ == "__main__":
    start()

# class Container(containers.DeclarativeContainer):

#     config = providers.Configuration()


# if __name__ == "__main__":
#     container = Container()

#     container.config.from_dict(
#         {
#             "aws": {
#                  "access_key_id": "KEY",
#                  "secret_access_key": "SECRET",
#              },
#         },
#     )

#     assert container.config() == {
#         "aws": {
#             "access_key_id": "KEY",
#             "secret_access_key": "SECRET",
#         },
#     }
#     assert container.config.aws() == {
#         "access_key_id": "KEY",
#         "secret_access_key": "SECRET",
#     }
#     assert container.config.aws.access_key_id() == "KEY"
#     assert container.config.aws.secret_access_key() == "SECRET"

# async def event_listener():
#     esdb_client = EventStoreDBClient(uri=EVENTSTORE)
#     meals_subscription = esdb_client.subscribe_to_stream(
#         stream_name="stream_one", from_end=True
#     )

#     while True:
#         for i, event in enumerate(meals_subscription):
#             data = event.data.decode("utf-8")
#             meal = Meal.model_validate_json(data)
#             print("type: ", event.type)

#             if event.type == "InsertMeal":
#                 MealsEventHandler.handle_insert_event()
#                 statement, args = MealMutations.insert_meal(
#                     meal=meal
#                 )

#                 MealTasks.insert_meal.send(
#                     statement=statement,
#                     args=args,
#                 )

#                 await asyncio.sleep(0.1)

#         print("-----------------------------> Committed \n")

#         print("-----------------------------> Committed \n")
