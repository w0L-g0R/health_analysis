# import asyncio
from typing import Annotated, Callable, Iterable

from taskiq import Context, TaskiqDepends, TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

type WorkerContainer = Annotated[Context, TaskiqDepends()]


# def register_tasks(broker: AioPikaBroker, tasks: Iterable[Callable]):
#     for task in tasks:
#         broker.register_task(func=task, task_name=task.__name__)


# meals_broker = meals_container.broker()


# register_tasks(
#     broker=meals_broker,
#     tasks=[MealsTasks.insert_meal],
# )


# @meals_broker.on_event(TaskiqEvents.WORKER_STARTUP)
# async def startup(state: TaskiqState) -> None:
#     state.meals_repository = meals_container.repository()


# @meals_broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
# async def shutdown(state: TaskiqState) -> None:
#     state.meals_repository = "close"
