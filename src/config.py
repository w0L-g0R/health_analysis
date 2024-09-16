import logging
import logging.config
from pathlib import Path

from toml import load

BASE_DIR_PATH = Path.cwd()

CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG_DICT = load(file)


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
