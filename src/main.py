# from config import CONFIG

# logging.config.dictConfig(CONFIG["logging"])
# logger = logging.getLogger(__name__)

# STOP_EVENT = asyncio.Event()
# FORMATTED_CONFIG = pformat(CONFIG, indent=4)


# @inject
# def handle_events(
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


# @inject
# def process(
#     event_data: str,
#     insert_event_handler: MealInsertEventHandler = Provide[
#         AppContainer.meals_container.insert_event_handler
#     ],
# ):
#     print("insert_event_handler: ", type(insert_event_handler))

#     # insert_event_handler.process(event_data)


# def main():
#     # logger.info(
#     #     f"\nStarting setup with config:\n{FORMATTED_CONFIG}\n"
#     # )
#     # logger.info(
#     #     f"Stopped asyncio event {id(STOP_EVENT)}: {STOP_EVENT.is_set()}"
#     # )

#     app = AppContainer(config=CONFIG)
#     app.init_resources()
#     app.wire(modules=[__name__])
#     app.check_dependencies()

#     logging.info(f"AppContainer set up: {id(app)}")

#     # Set up signals that stops the event loop in case of a container/pod shutdown
#     signal(SIGINT, lambda x: STOP_EVENT.set())
#     signal(SIGTERM, lambda x: STOP_EVENT.set())

#     # broker = app.broker()

#     # dramatiq.set_broker(broker)

#     # logging.info(f"Broker set up: {dramatiq.get_broker()}")

#     process.send("hi")

#     # try:
#     #     asyncio.run(start_event_subscriptons())

#     # except KeyboardInterrupt:
#     #     logging.error("Application interrupted by keyboard.")


import asyncio

from bootstrap import meals_broker

# meals_broker = AioPikaBroker(url="amqp://guest:guest@127.0.0.1:5672")
# meals_broker.register_task(MealsTasks.insert_meal, "MealInsert")


async def main():
    print("Main running")
    # await asyncio.sleep(0)

    await meals_broker.startup()
    print("meals_broker: ", meals_broker)

    task = meals_broker.find_task(task_name="MealInsert")
    print("meals_broker: ", meals_broker)
    print("task: ", task)

    # task = broker.find_task(task_name="get_client_task")

    # print("task: ", task)
    # task
    if task:
        _task = await task.kiq("event")
        res = await _task.wait_result()
        print("res: ", res)
    # print("get_client_task: ", get_client_task)

    # get_res = await get_client_task.wait_result()

    # print(f"Got client value: {get_res.is_err}")

    # await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
