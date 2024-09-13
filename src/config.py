import os
from pathlib import Path

import toml
from dotenv import load_dotenv

# path = os.path.join(os.getcwd(), "pg_service.conf")


def get_config_dict_from_toml(toml_config_file: str) -> dict:
    with open(toml_config_file, "r") as file:
        return toml.load(file)


CONFIG_FILE = Path(__file__).parent / "config.toml"
CONFIG = get_config_dict_from_toml(CONFIG_FILE)


# os.environ["PGSERVICEFILE"] = path

# load_dotenv()

# TIMESCALE_DB = os.getenv("TIMESCALE_DB")
# EVENTSTORE = os.getenv("EVENTSTORE")
# RABBIT_MQ = os.getenv("RABBIT_MQ")
# REDIS_RESULTS = os.getenv("REDIS_RESULTS")

# MEALS_QUEUE = os.getenv("MEALS_QUEUE")
# HEALTH_QUEUE = os.getenv("HEALTH_QUEUE")

# MEALS_TABLE = os.getenv("MEALS_TABLE")
# HEALTH_TABLE = os.getenv("HEALTH_TABLE")
