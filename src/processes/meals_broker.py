from taskiq import TaskiqEvents, TaskiqState
from src.config import CONFIG_DICT
from src.dependencies.meals.container import MealsContainer
from src.tasks.meal_tasks import MealTasks

meals_container = MealsContainer()
meals_container.config.from_dict(CONFIG_DICT)
meals_container.init_resources()
meals_broker = meals_container.broker()


# @meals_broker.on_event(TaskiqEvents.WORKER_STARTUP)
# async def startup(state: TaskiqState) -> None:
#     # Here we store connection pool on startup for later use.
#     state.redis = "redis"


print("meals_broker: ", meals_broker.get_all_tasks())
print("meals_broker: ", meals_broker.find_task(task_name=MealTasks.INSERT.value))
print("MealTasks.INSERT.value: ", MealTasks.INSERT.value)
print("state: ", meals_broker.state)
