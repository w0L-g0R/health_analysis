from src.config.config import CONFIG_DICT, get_module_path
from src.dependencies.meals.meals_container import MealsContainer

meals_container = MealsContainer()
meals_container.config.from_dict(CONFIG_DICT)
meals_container.init_resources()
meals_broker = meals_container.broker()

if __name__ == "__main__":
    meals_broker.start_workers_process(__file__)
