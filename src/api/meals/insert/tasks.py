from dependency_injector.wiring import Provide, inject
from dramatiq import Message, actor

from api.meals.insert.handler import MealInsertEventHandler
from dependencies.app import AppContainer


@actor
@inject
async def process_insert_meal_event(
    event_data: Message,
    insert_event_handler: MealInsertEventHandler = Provide[
        AppContainer.meals_container.insert_event_handler
    ],
):
    # print("handler event", insert_event_handler)
    # insert_event_handler()
    # .process(event_data)
    # handler = insert_event_handler()
    # handler.
    # print("handler: ", handler())
    # handler.process(event_data)
    # handler.pri()
    await insert_event_handler.process(event_data)
