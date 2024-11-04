import logging
from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, Provider, inject
from faker.generator import random
from taskiq import TaskiqEvents, TaskiqState, TaskiqDepends

# from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import add_meal_task
from src.adapters.spi.persistence.time_scale_db.meals.meals_repository import (
    MealsRepository,
)
from src.config.config import CONFIG_DICT
from src.containers.brokers_container import BrokersContainer
from src.containers.meals_container import MealsContainer

# CONFIG_DICT_PATH = Path.cwd().parents[0] / "config.toml"
# CONFIG_DICT = get_config_dict_from_toml_file_path(CONFIG_DICT_PATH)

brokers_container = BrokersContainer()
brokers_container.config.from_dict(CONFIG_DICT)

meals_broker = brokers_container.meals_broker()
# meals_broker.register_task(lambda event_data: add_meal_task, task_name="add_meal_task")

# meals_broker.add_dependency_context({"container": MealsContainer})
# meals_broker.add_event_handler(TaskiqEvents.WORKER_STARTUP, startup)


@meals_broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup_meals_broker(state: TaskiqState):
    container = MealsContainer()
    container.config.from_dict(CONFIG_DICT)
    await container.init_resources()

    state.repository = await container.repository()
    state.validators = container.validators()
    state.model = container.model

    print("State:", state)
