# from esdbclient import CatchupSubscription
# import asyncio


# from src.config.config import CONFIG_DICT, setup_logging
# from dependency_injector.wiring import Provide, inject

# from src.dependencies.events_bus import EventBusContainer, MealEventBusContainer
# from src.brokers.meals_broker import meals_broker


# STOP_EVENT = asyncio.Event()


# async def handle_subscription_events(
#     subscription: CatchupSubscription,
# ):
#     while not STOP_EVENT.is_set():
#         logging.info(f"Start listening to events of subscription {id(subscription)}")

#         try:
#             for event in subscription:
#                 logging.info(
#                     f"Received event from subscription {id(subscription)}:\n{pformat(event, indent=2)}"
#                 )

#                 match event.type:
#                     case "MealInsert":
#                         # await insert_event_handler.validate_and_serialize(event)
#                         # insert_event_handler.process(event.data.decode("utf-8"))
#                         # process_insert_meal_event.send(
#                         #     event.data.decode("utf-8"),
#                         # )
#                         pass
#                         # process(event.data.decode("utf-8"))
#                     case _:
#                         print("No matching type")

#             # Prevent CPU overuse
#             # await asyncio.sleep(0.1)

#         except Exception as e:
#             logging.error(f"Error in handle_events:{e}")
#             raise e

# setup_logging()
import asyncio
import logging

from src.application.handlers.meals_events_handler import MealsEventsHandler
from src.brokers import meals_broker
from src.containers.meals import MealsContainer
from src.config.config import CONFIG_DICT, setup_logging
from dependency_injector.wiring import Provide, inject

from asyncio import gather

from src.services.meals_service import MealsService

setup_logging()
logger = logging.getLogger(__name__)


@inject
async def main(
    meal_service: MealsService = Provide[MealsContainer.service],
):
    # Start brokers
    for broker in [meals_broker]:
        await broker.startup()
        logger.info(f"\nStarting {broker.__repr__()}")

    #

    try:
        await gather(meal_service.handle_events())

    except Exception as e:
        logging.error(f"Error on handle_events: {e}")

    finally:
        # meal_events_client.close()
        await meals_broker.close()
        # STOP_EVENT.set()

    #     logging.info(f"Stopped asyncio event {id(STOP_EVENT)}: {STOP_EVENT.is_set()}")
    #     await asyncio.sleep(0.25)

    #     client.close()

    # logging.info(f"Closed event bus client {id(client)}: {client._is_closed}")

    # shutdown()

    # tasks = meals_broker.get_all_tasks()
    # print("MealTasks.INSERT.value: ", MealTasks.INSERT.value)
    # print("tasks: ", tasks)

    # task = meals_broker.find_task(task_name=MealTasks.INSERT.value)
    # print("task: ", task)

    # event_insert_meal = InsertMealEvent(
    #     user_id=uuid4(),
    #     meal_name="test_meal",
    #     calories=float("{:.2f}".format(abs(random()))),
    # )

    # if task:
    #     _task = await task.kiq(event_insert_meal)
    #     # _task2 = await task.kiq("event2")
    #     res = await _task.wait_result()
    #     # res2 = await _task2.wait_result()
    #     print("res: ", res)
    #     # print("res2: ", res2)

    # print("get_client_task: ", get_client_task)

    # get_res = await get_client_task.wait_result()

    # print(f"Got client value: {get_res.is_err}")

    # await meals_broker.shutdown()


if __name__ == "__main__":
    meals_container = MealsContainer()
    meals_container.config.from_dict(CONFIG_DICT)
    meals_container.init_resources()
    meals_container.wire(modules=[__name__, MealsEventsHandler])
    asyncio.run(main())


# @inject
# def shutdown(
#     eventbus_client: EventBusContainer = Provide[AppContainer.eventbus_client],
#     meals_repository: MealsRepository = Provide[
#         AppContainer.meals_container.repository
#     ],
# ):
#     STOP_EVENT.set()

#     logging.info(f"Stopped asyncio event {id(STOP_EVENT)}: {STOP_EVENT.is_set()}")
#     # await asyncio.sleep(0.25)

#     eventbus_client.close()

#     logging.info(
#         f"Closed event bus client {id(eventbus_client)}: {eventbus_client._is_closed}"
#     )

#     meals_repository.close()

# def main():

#     # Set up signals that stops the event loop in case of a container/pod shutdown
#     signal(SIGINT, lambda x: STOP_EVENT.set())
#     signal(SIGTERM, lambda x: STOP_EVENT.set())


# @inject
# async def start_event_subscriptons(
#     eventbus=Provide[AppContainer.eventbus],
#     # insert_event_handler: MealInsertEventHandler = Provide[
#     #     AppContainer.meals_container.insert_event_handler
#     # ],
# ):
#     try:
#         # handler = insert_event_handler
#         # print("APP handler: ", handler)

#         await asyncio.gather(
#             handle_events(
#                 eventbus.meals_subscription(),
#             ),
#             # handle_events(health_subscription, meals_event_handler),
#         )

#     except Exception as e:
#         logging.error(f"Error in start_event_subscriptons: {e}")

#     finally:
#         shutdown()
