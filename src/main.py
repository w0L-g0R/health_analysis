import asyncio
from multiprocessing import Process
from time import sleep as time_sleep
from typing import Annotated

from dependency_injector.providers import Resource
from dependency_injector.wiring import Provider, inject
from esdbclient.common import AbstractCatchupSubscription
from taskiq import TaskiqEvents, TaskiqState, TaskiqDepends
from taskiq_aio_pika import AioPikaBroker

from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import add_meal_task
from src.adapters.api.tasks.taskiq.meal_tasks import MealTasks, TaskiqTask

# from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import add_one

# from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import add_one
from src.adapters.spi.persistence.time_scale_db.meals.meals_repository import (
    MealsRepository,
)
from src.brokers.bootstrap import start_meals_broker

# from src.brokers.bootstrap import start_health_broker, start_meals_broker
from src.brokers.meals_broker import meals_broker
from src.config.config import CONFIG_DICT
from src.containers.event_client_container import EventClientContainer
from src.containers.meals_container import MealsContainer


# test_meals_broker = AioPikaBroker(
#     url="amqp://guest:guest@localhost:5672", queue_name="meals"
# )


# def start_test_meals_broker():
#     worker_args = WorkerArgs(
#         broker="src.main:test_meals_broker",
#         modules=["src.main"],
#     )
#
#     print("Meals broker is running")
#     run_worker(worker_args)


# @inject
# async def handle_meal_events(
#     event_client_container: EventClientContainer = Provide[EventClientContainer],
#     meals_container: MealsContainer = Provide[MealsContainer],
# ):
#     await meals_broker.startup()
#
#     meals_subscription = event_client_container.meal_events_subscription()
#     meals_event_handler = meals_container.meals_event_handler()
#     meal_tasks = MealTasks(add_meal=meals_broker.find_task("add_meal_task"))
#
#     await meals_event_handler.handle_events(
#         subscription=meals_subscription,
#         add_meal_task=meal_tasks.add_meal,
#     )


async def main():

    # meals_broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, startup)
    # meals_broker.add_dependency_context({"meals_container": MealsContainer})

    # meals_broker.add_dependency_context({"container": MealsContainer})

    await meals_broker.startup()
    # t = meals_broker.register_task(
    #     lambda data: add_meal_task, task_name=MealTasks.ADD_MEAL
    # )
    # r = meals_broker.context.repository

    meal_tasks = {
        k: TaskiqTask(task=v) for k, v in meals_broker.get_all_tasks().items()
    }

    print("meal_tasks", meal_tasks)
    # t = meals_broker.find_task("add_meal_task")

    # meals_tasks = await meals_container.meal_tasks()
    # meals_tasks.add_meal.set_task(meals_broker.find_task("add_meal_task"))
    # print("t", t)
    # r = await t.kiq(data="datahhh")
    # r = await t.kiq(data="datahhh")
    # r = await t.kiq(data="datahhh")

    # await meals_broker.startup()

    # print("meals_broker main", meals_broker)
    # meals_broker.register_task(lambda x: add_one, task_name="add_one")
    # add_one_task = TaskiqTask()
    # t.task = add_one

    # t = await add_one_task.execute()
    # r = await t.wait_result()
    # print(r)
    # print(t)

    # meals_broker.register_task(t, task_name="add_one")
    # meal_tasks = MealTasks(add_one=))

    event_client_container = EventClientContainer()
    event_client_container.config.from_dict(CONFIG_DICT)
    event_client_container.init_resources()

    meals_event_handler = event_client_container.meal_events_handler()

    await asyncio.gather(*[meals_event_handler.handle_events(tasks=meal_tasks)])

    await meals_broker.shutdown()


async def process_meal_events(
    broker: AioPikaBroker,
    subscription: AbstractCatchupSubscription,
    meals_container: MealsContainer,
):

    # await meals_container.init_resources()
    # c = await meals_container.connection_pool.init()
    # print(c)
    # r = await meals_container.repository.init()
    # print(r)
    # await c.add(
    #     (
    #         datetime.now(),
    #         "faaf6aa2-7afb-4a95-8379-1febe41caf5c",
    #         "faaf6aa2-7afb-4a95-8379-1febe41caf5cuser_id",
    #         "meal_name",
    #         12,
    #     )
    # )

    # event_handler = meals_container.event_handler()

    # add_one_task = broker.find_task("add_one")
    #
    # print("add_one_task", add_one_task)

    # t = await dyn_task.kiq(x=1)
    # t = await add_one_task.kiq()
    # r = await t.wait_result()
    # print(r)
    # print(t)

    # meals_subscription = event_client_container.meal_events_subscription()
    # meals_container.init_resources()
    # print("event_handler", event_handler)

    # meals_event_handler = meals_container.event_handler()
    # meal_tasks = MealTasks(add_meal=meals_broker.find_task("add_meal_task"))

    # print(meals_broker.state)
    # print(meals_broker.read_conn)

    # r = await t.wait_result()
    # print(add_one_task)
    # t = await add_one_task.kiq()
    # r = await t.wait_result()

    # await asyncio.gather(
    #     *[
    #         handle_meal_events(),
    #     ]
    # )

    # await asyncio.sleep(2)
    # #
    pass


if __name__ == "__main__":
    # multiprocessing.log_to_stderr(logging.DEBUG)

    # test_meal_worker_process = Process(target=start_test_meals_broker)
    meal_worker_process = Process(target=start_meals_broker)
    # health_worker_process = Process(target=start_health_broker)
    #
    # test_meal_worker_process.start()
    meal_worker_process.start()

    time_sleep(1)
    # health_worker_process.start()

    # meal_worker_process.join()

    asyncio.run(main())

    # Wait for the meal_worker_process to complete
    meal_worker_process.join()

    # asyncio.gather(
    #     *[
    #         process_meal_events(subscription, meal_events_handler),
    #     ]
    # )
