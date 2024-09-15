import logging
import logging.config
from pathlib import Path

from toml import load

BASE_DIR_PATH = Path.cwd() / "src"

CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG_DICT = load(file)


def setup_logging():
    logging.config.dictConfig(CONFIG_DICT["logging"])
