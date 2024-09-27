import logging
from pathlib import Path

# from src.adapters.api.tasks.taskiq.meals.add_meal_task import add_one
from src.config.config import CONFIG_DICT
from src.containers.brokers_container import BrokersContainer

# CONFIG_DICT_PATH = Path.cwd().parents[0] / "config.toml"
# CONFIG_DICT = get_config_dict_from_toml_file_path(CONFIG_DICT_PATH)

brokers_container = BrokersContainer()
brokers_container.config.from_dict(CONFIG_DICT)

meals_broker = None

if meals_broker is None:
    meals_broker = brokers_container.meals_broker()
