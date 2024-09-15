from pathlib import Path
from typing import Annotated
from uuid import uuid4
from redis import ConnectionPool
from taskiq_aio_pika import AioPikaBroker
from toml import load

from api.meals.tasks import MealsTasks


from taskiq import TaskiqEvents, TaskiqState


CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG = load(file)


# meals_broker = meals_container.broker()


# state = TaskiqState()
# state["db"] = uuid4()
# broker.state = state
# print("broker.state: ", broker.state)
# # broker.register_task(MealsTasks.insert_meal, "MealInsert")
# broker.register_task(MealsTasks.insert_meal, "MealInsert")
# # from taskiq import Context, TaskiqDepends

broker = AioPikaBroker(url=CONFIG["dsn"]["rabbitmq"]["url"])
from bootstrap import db


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    # broker.add_dependency_context({"database": db})
    print("db: ", db)
    state.db = db


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
