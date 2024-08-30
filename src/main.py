import logging
import sys
from pathlib import Path
from pprint import pprint

import toml
from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)


class Core(DeclarativeContainer):
    config_file = Path(__file__).parent / "config.toml"
    config = providers.Configuration()

    logging = providers.Resource(
        logging.basicConfig,
        level=logging.INFO,
        stream=sys.stdout,
    )

    @classmethod
    def get_config_dict_from_toml_file(cls):
        with open(cls.config_file, "r") as file:
            data = toml.load(file)
            return data

    @classmethod
    def configure(cls):
        toml_data = cls.get_config_dict_from_toml_file()
        print("toml_data: ", toml_data)

        cls.config.from_dict(toml_data)

        # logging_config = get_logging_config_from(toml_data)
        # logging_config = {"logging": logging_config}
        # print("\nconfig:\n")
        # pprint(logging_config)

        # cls.logging = providers.Resource(
        #     logging.config.dictConfig,
        #     config=logging_config,
        # )

        # pprint(
        #     f"cls.logging: {cls.logging()}",
        # )

        # toml_data = {
        #     "logging": {
        #         "version": 1,
        #         "formatters": {
        #             "formatter": {
        #                 "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        #             }
        #         },
        #         "handlers": {
        #             "console": {
        #                 "class": "logging.StreamHandler",
        #                 "level": "DEBUG",
        #                 "formatter": "formatter",
        #                 "stream": "ext://sys.stderr",
        #             }
        #         },
        #         "root": {
        #             "level": "DEBUG",
        #             "handlers": ["console"],
        #         },
        #     },
        #     "databases": {},
        #     "timescaledb": {
        #         "host": "localhost",
        #         "port": "5433",
        #         "dbname": "meals",
        #         "user": "user",
        #         "password": "password",
        #     },
        # }

        # cls.logging = await providers.Resource(
        #     dictConfig,
        #     config=toml_data["logging"],
        # ).init()
        # cls.logging = providers.Resource(
        #     dictConfig,
        #     config=toml_data["logging"],
        # ).init()
        # cls.logging.__init__()

        # print("cls.logging: ", cls.logging)


class ApplicationContainer(DeclarativeContainer):
    core = providers.Container(Core)

    config = providers.Configuration(
        yaml_files=["config.yml"]
    )

    pass


def start():
    print("Started data store event listener")

    Core.configure()

    pprint(f"Core.config: {Core.config}")

    # asyncio.run(event_listener())
    application = ApplicationContainer()
    application.core.init_resources()
    application.wire(modules=[__name__])

    print(
        "application.dependencies: ", application.dependencies
    )


if __name__ == "__main__":
    start()

# class Container(containers.DeclarativeContainer):

#     config = providers.Configuration()


# if __name__ == "__main__":
#     container = Container()

#     container.config.from_dict(
#         {
#             "aws": {
#                  "access_key_id": "KEY",
#                  "secret_access_key": "SECRET",
#              },
#         },
#     )

#     assert container.config() == {
#         "aws": {
#             "access_key_id": "KEY",
#             "secret_access_key": "SECRET",
#         },
#     }
#     assert container.config.aws() == {
#         "access_key_id": "KEY",
#         "secret_access_key": "SECRET",
#     }
#     assert container.config.aws.access_key_id() == "KEY"
#     assert container.config.aws.secret_access_key() == "SECRET"

# async def event_listener():
#     esdb_client = EventStoreDBClient(uri=EVENTSTORE)
#     meals_subscription = esdb_client.subscribe_to_stream(
#         stream_name="stream_one", from_end=True
#     )

#     while True:
#         for i, event in enumerate(meals_subscription):
#             data = event.data.decode("utf-8")
#             meal = Meal.model_validate_json(data)
#             print("type: ", event.type)

#             if event.type == "InsertMeal":
#                 MealsEventHandler.handle_insert_event()
#                 statement, args = MealMutations.insert_meal(
#                     meal=meal
#                 )

#                 MealTasks.insert_meal.send(
#                     statement=statement,
#                     args=args,
#                 )

#                 await asyncio.sleep(0.1)

#         print("-----------------------------> Committed \n")

#         print("-----------------------------> Committed \n")
