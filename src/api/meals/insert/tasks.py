from dramatiq import actor

from api.meals.insert.handler import MealInsertEventHandler


@actor
def process_insert_meal_event(
    insert_event_handler: MealInsertEventHandler,
):
    # h = insert_event_handler()
    # print("h: ", h)

    # Check if the insert_event_handler is an instance of MealInsertEventHandler
    if isinstance(
        insert_event_handler, MealInsertEventHandler
    ):
        print("Handler successfully injected!")
    else:
        print(
            f"Handler injection failed: {insert_event_handler}"
        )

    print("insert_event_handler: ", insert_event_handler)

    # insert_event_handler.process(event_data)
