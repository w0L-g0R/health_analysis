import logging
import logging.config
from pathlib import Path
from pprint import pformat

from toml import load
from src.config.validation import validate_config

BASE_DIR_PATH = Path.cwd()
# print(Path(__file__).parents[1])
CONFIG_FILE_PATH = BASE_DIR_PATH / "src" / "config.toml"


# def get_config_dict_from_toml_file_path(path: Path):
#     # with open(path, "r") as file:
#     #     return load(file)
#     print("Path", path)
#
#     with open(path, "r") as file:
#         config_dict = load(file)
#         uris = validate_config(config_dict)
#         connections = dict(
#             timescaledb=uris.get("uri_timescale_db"),
#             eventstoredb=uris.get("uri_event_store_db"),
#             rabbitmq=uris.get("uri_rabbit_mq"),
#         )
#
#         config_dict["connections"] = connections
#
#         return config_dict
#         # print(pformat(CONFIG_DICT))


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
