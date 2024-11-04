from taskiq import TaskiqEvents, TaskiqState

from src.config.config import CONFIG_DICT
from src.containers.brokers_container import BrokersContainer
from src.containers.meals_container import MealsContainer

brokers_container = BrokersContainer()
brokers_container.config.from_dict(CONFIG_DICT)

meals_broker = brokers_container.meals_broker()


@meals_broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup_meals_broker(state: TaskiqState):

    container = MealsContainer()
    container.config.from_dict(CONFIG_DICT)
    await container.init_resources()

    state.repository = await container.repository()
    state.validators = container.validators()
    state.model = container.model

    # print("State:", state)
