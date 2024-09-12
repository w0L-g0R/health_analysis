# import asyncio

from typing import Callable

from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from meals_tasks import MealsTasks
from wiring import meals_container


def register_tasks(broker: AioPikaBroker, tasks: Callable[]):
    for task in tasks:
        broker.register_task(func=task, task_name=task.__name__)]


meals_broker = meals_container.broker()

register_tasks(
    broker=meals_broker,
    task=MealsTasks.insert_meal,
)


@meals_broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    state.meals_repository = meals_container.repository()


@meals_broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    state.meals_repository = "close"
