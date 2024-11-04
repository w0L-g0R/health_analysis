import asyncio
from multiprocessing import Process
from time import sleep as time_sleep

from dependency_injector.wiring import Provide, inject
from taskiq.cli.worker.args import WorkerArgs
from taskiq.cli.worker.run import run_worker

from src.brokers.meals_broker import meals_broker
from src.config.config import CONFIG_DICT
from src.containers.event_client_container import EventClientContainer
from src.handlers.meal_events_handler import MealsEventsHandler
from src.tasks.meals.add_meal_task import meal_broker_health_check
from src.tasks.taskiq_task import TaskiqTask


@inject
async def handle_meal_events(
    meal_events_handler: MealsEventsHandler = Provide[
        EventClientContainer.meal_events_handler
    ],
):
    print("Started broker")

    await meals_broker.startup()
    _ = meals_broker.register_task("meal_broker_health_check", meal_broker_health_check)

    meal_tasks = {
        k: TaskiqTask(task=v) for k, v in meals_broker.get_all_tasks().items()
    }

    print("Tasks:", meal_tasks)
    await meal_events_handler.handle_events(tasks=meal_tasks)
    await meals_broker.shutdown()


async def start_event_listener():

    container = EventClientContainer()
    container.config.from_dict(CONFIG_DICT)
    container.init_resources()
    container.wire(modules=[__name__])

    await asyncio.gather(*[handle_meal_events()])


def start_meal_workers():
    run_worker(
        WorkerArgs(
            broker="src.brokers.meals_broker:meals_broker",
            modules=["src.brokers.meals_broker"],
            workers=3,
        )
    )


if __name__ == "__main__":
    # multiprocessing.log_to_stderr(logging.DEBUG)

    # test_meal_worker_process = Process(target=start_test_meals_broker)
    meal_worker_process = Process(target=start_meal_workers)

    # health_worker_process = Process(
    #     target=run_worker(
    #         WorkerArgs(
    #             broker="src.brokers.health_broker:health_broker",
    #             modules=["src.brokers.health_broker"],
    #         )
    #     )
    # )

    # health_worker_process = Process(target=start_health_broker)
    #
    # test_meal_worker_process.start()
    meal_worker_process.start()

    time_sleep(1)
    # health_worker_process.start()

    # meal_worker_process.join()

    asyncio.run(start_event_listener())

    # Wait for the meal_worker_process to complete
    meal_worker_process.join()
