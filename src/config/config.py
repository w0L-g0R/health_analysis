import logging
import logging.config
from pathlib import Path
from pprint import pformat

from toml import load
from src.config.validation import validate_config

BASE_DIR_PATH = Path.cwd()
print(Path(__file__).parents[1])
CONFIG_FILE_PATH = BASE_DIR_PATH / "src" / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG_DICT = load(file)
    uris = validate_config(CONFIG_DICT)
    connections = dict(
        timescaledb=uris.get("uri_timescale_db"),
        eventstoredb=uris.get("uri_event_store_db"),
        rabbitmq=uris.get("uri_rabbit_mq"),
    )
    CONFIG_DICT["connections"] = connections
    # print(pformat(CONFIG_DICT))


def get_module_path(file: str):
    return (
        Path(file)
        .resolve()
        .relative_to(BASE_DIR_PATH)
        .with_suffix("")
        .as_posix()
        .replace("/", ".")
    )


def setup_logging():
    logging.config.dictConfig(CONFIG_DICT["logging"])
