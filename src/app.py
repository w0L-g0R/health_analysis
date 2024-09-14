from pathlib import Path
from uuid import uuid4

from toml import load

from dependencies.app import AppContainer

CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG = load(file)

global app_container
app_container = AppContainer(config=CONFIG)


def get_db():
    db = uuid4()
    return db


global db
db = get_db()
