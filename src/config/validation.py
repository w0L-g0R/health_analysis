from pprint import pformat

from pydantic import BaseModel, ConfigDict, PostgresDsn, ValidationError
from pydantic_core import Url
import pytest

from src.config.connection_strings import (
    ConnectionStringTimescaleDb,
    EventStoreDBConnectionString,
    RabbitMQConnectionString,
)
from src.config.exceptions import (
    EmptyValueError,
    EmptyValueErrorMessages,
    InvalidConfigurationError,
)


class FieldValidator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


@pytest.mark.validation
def validate_config(config: dict) -> dict[str, PostgresDsn | Url | None]:
    try:
        match config:
            case {
                "credentials": {
                    "timescaledb": timescaledb_config,
                    "eventstoredb": eventstoredb_config,
                    "rabbitmq": rabbitmq_config,
                },
                "databases": databases_config,
                "streams": streams_config,
                "queues": queues_config,
                "exchanges": exchanges_config,
                "events": events_config,
                "logging": dict(),
            }:
                # Validate the dns configurations using Pydantic models
                connection_timescale_db = ConnectionStringTimescaleDb(
                    **timescaledb_config
                )
                connection_event_store_db = EventStoreDBConnectionString(
                    **eventstoredb_config
                )
                connection_rabbit_mq = RabbitMQConnectionString(**rabbitmq_config)

                for key, value in streams_config.items():
                    if not value:
                        raise EmptyValueError(
                            f"{EmptyValueErrorMessages.STREAMS.value} {key}"
                        )

                for key, value in queues_config.items():
                    if not value:
                        raise EmptyValueError(
                            f"{EmptyValueErrorMessages.QUEUES.value} {key}"
                        )

                for key, value in exchanges_config.items():
                    if not value:
                        raise EmptyValueError(
                            f"{EmptyValueErrorMessages.EXCHANGES.value} {key}"
                        )

                for key, value in events_config.items():
                    for sub_key, sub_value in value.items():
                        if not sub_value:
                            raise EmptyValueError(
                                f"{EmptyValueErrorMessages.EVENTS.value} {key}.{sub_key}"
                            )

                for key, value in databases_config.items():
                    if not value:
                        raise EmptyValueError(
                            f"{EmptyValueErrorMessages.DATABASES.value} {key}"
                        )

            case _:
                raise InvalidConfigurationError(
                    f"Invalid configuration: {pformat(config)}"
                )

        return {
            "uri_timescale_db": connection_timescale_db.uri,
            "uri_event_store_db": connection_event_store_db.uri,
            "uri_rabbit_mq": connection_rabbit_mq.uri,
        }

    except ValidationError as e:
        raise InvalidConfigurationError(f"PydanticCustomError: {e}")
