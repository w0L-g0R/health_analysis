import asyncio
from pprint import pprint

from dependency_injector.wiring import Provide, inject
from psycopg2.pool import SimpleConnectionPool

from config import CONFIG
from container.app import AppContainer
from container.eventbus import EventBus

# async def subscribe_to_stream():
#     async with client.subscribe_to_stream(stream_name) as subscription:
#         while True:
#             async for event in subscription:
#                 print(f"Received event from {stream_name}: {event}")
#             await asyncio.sleep(2)  # Prevent CPU overuse


@inject
def test(
    timescale_db_pool: SimpleConnectionPool = Provide[
        AppContainer.pools.timescale_db_pool
    ],
) -> None:
    #     pool = next(timescale_db_pool)
    #     print("pool: ", pool)
    #     conn = pool.getconn()
    #     print("conn: ", conn)
    return


async def start_event_handler(subscription):
    switch = True
    while switch == True:
        print(f"Received event from {subscription}")
        switch = False
        # await asyncio.sleep(2)


@inject
async def main(
    eventbus: EventBus = Provide[AppContainer.eventbus],
):
    subscription = eventbus.subscription.meals()
    print("subscription: ", subscription)
    # sub = client.subscribe_to_stream(stream_name="meals")
    # print("client: ", client)

    # sub = subscription.subscription()().subscribe_to_stream(
    #     stream_name="meals"
    # )
    # print("sub: ", eventbus.subscription())

    # print("sub: ", sub)

    await asyncio.gather(
        # start_event_handler(
        # subscriptions.subscription("meals")
        # ),
    )

    # await client.client.close()


def start():
    print("\nStart IOC container setup with config:\n")
    pprint(
        CONFIG,
    )

    app = AppContainer(config=CONFIG)
    app.init_resources()
    app.wire(modules=[__name__])
    app.check_dependencies()
    # logging.info("\nCheck:\n")

    # test()
    asyncio.run(main())


if __name__ == "__main__":
    start()

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
