from config import CONFIG_DICT
from dependencies.domain.meals import MealsContainer


meals_container = MealsContainer()
meals_container.config.from_dict(CONFIG_DICT)
meals_container.init_resources()
