import asyncio

from config import CONFIG_DICT
from dependencies.meals import MealsContainer
from asyncio import run
# from dependency_injector.wiring import Provide, inject


async def init_resources(container):
    await container.init_resources()


async def init_broker(container):
    broker = container.broker()
    return broker


container = MealsContainer()
container.config.from_dict(CONFIG_DICT)
run(init_resources(container))
broker = run(init_broker(container))
print("broker: ", broker)
