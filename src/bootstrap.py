from pathlib import Path
from toml import load

from api.meals.tasks import MealsTasks

from dependencies.app import AppContainer
from dependencies.database import DB

CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG = load(file)

app_container = AppContainer(config=CONFIG)
app_container.init_resources()
app_container.wire(modules=[__name__])

meals_container = app_container.meals_container()

meals_broker = meals_container.broker()
meals_database = meals_container.database()
meals_broker.add_dependency_context({"database": meals_database})

meals_broker.register_task(func=MealsTasks.insert_meal, task_name="MealInsert")


print("meals_broker: ", meals_broker)
