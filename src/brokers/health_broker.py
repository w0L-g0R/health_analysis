from src.config.config import CONFIG_DICT
from src.containers.brokers_container import BrokersContainer


brokers_container = BrokersContainer()
brokers_container.config.from_dict(CONFIG_DICT)

health_broker = brokers_container.health_broker()
