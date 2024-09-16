# from src.config import CONFIG_DICT
# from src.dependencies.meals.container import MealsContainer

# meals_container = MealsContainer()
# meals_container.config.from_dict(CONFIG_DICT)
# meals_container.init_resources()
# meals_broker = meals_container.meals_broker()

# meals_broker.register_task(
#     func=insert_meal,
#     name=MealTasks.INSERT.value,
# )

# meals_broker.add_event_handler(
#     event=TaskiqEvents.WORKER_STARTUP,
#     handler=lambda state: startup_worker_event_handler(
#         state=state,
#         database=meals_container.database,
#         events=meals_container.events,
#         query_factories=meals_container.query_factories,
#     ),
# )

# meals_broker.add_event_handler(
#     event=TaskiqEvents.WORKER_SHUTDOWN,
#     handler=lambda state: shutdown_worker_event_handler(state=state),
# )
