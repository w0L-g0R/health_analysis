import asyncio
from typing import Annotated

from taskiq import (
    Context,
    TaskiqDepends,
    TaskiqEvents,
    TaskiqState,
)
from taskiq_aio_pika import AioPikaBroker

from api.meals.tasks import MealsTasks
from config import CONFIG_DICT
from dependencies.meals import MealsContainer


async def init_broker() -> AioPikaBroker:
    meals_container = MealsContainer()
    meals_container.config.from_dict(CONFIG_DICT)
    meals_database = await meals_container.database()

    meals_broker = meals_container.broker()
    # meals_database = meals_container.database()

    state = TaskiqState()
    state["database"] = meals_database
    meals_broker.state = state
    # meals_broker.add_dependency_context(
    #     {"state.db": meals_database}
    # )

    meals_broker.register_task(
        MealsTasks.insert_meal,
        MealsTasks.insert_meal.__name__,
    )

    # meals_broker.add_event_handler(
    #     event=TaskiqEvents.WORKER_STARTUP,
    #     handler=meals_broker.state.database.close,
    # )

    return meals_broker


def close_db(context: Annotated[Context, TaskiqDepends()]):
    context.database.close()


meals_broker = asyncio.run(init_broker())

# state = TaskiqState()
# state["db"] = uuid4()
# broker.state = state
# print("broker.state: ", broker.state)
# broker.register_task(MealsTasks.insert_meal, "MealInsert")
# # from taskiq import Context, TaskiqDepends

# meals_broker = AioPikaBroker(
#     url="amqp://guest:guest@127.0.0.1:5672"
# )

# meals_container = MealsContainer()

# meals_container.config.from_dict(CONFIG_DICT)
# asyncio.wait(meals_container.init_resources())
# meals_broker = meals_container.broker()


# meals_container = MealsContainer()
# meals_container.config.from_dict(CONFIG_DICT)
# meals_container.database()
# meals_broker = meals_container.broker()


# Run the async function

# print("meals_container.config", meals_container.config())
# config = meals_container.config()
# # from bootstrap import db


# meals_broker = AioPikaBroker(url=config["dsn"]["rabbitmq"])
@meals_broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    await state.database.close()


# @broker.on_event(TaskiqEvents.WORKER_STARTUP)
# async def startup(state: TaskiqState) -> None:
#     from bootstrap import app_container

#     #     # app_container = AppContainer(config=CONFIG)
#     #     # pool = await app_container.pool()
#     #     # app_container.database.enable_async_mode()
#     #     # print("pool: ", id(pool))
#     #     # app_container.init_resources()
#     #     # app_container.wire(modules=[__name__])
#     #     # print("app_container: ", app_container)
#     app_container.init_resources()
#     app_container.wire(modules=[__name__])
#     state.container = app_container
#     print("app_container: ", app_container.pool)


#     # meals_container = app_container.meals_container()
#     # meals_database = meals_container.database()
#     # print("meals_database: ", meals_database)
#     # print("state", state)

#     # state.broker.register_task(func=MealsTasks.insert_meal, task_name="MealInsert")


# @broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
# async def shutdown(state: TaskiqState) -> None:
#     print(state)


# meals_broker.add_dependency_context({"database": meals_database})


# print("meals_broker: ", broker)
# print("meals_broker: ", broker)
# print("meals_broker: ", broker)
# print("meals_broker: ", broker)
# print("meals_broker: ", broker)
# print("meals_broker: ", broker)
