from pydantic import ValidationError
import pytest
from src.config.connection_string import (
    ConnectionStringTimescaleDb,
    EventStoreDBConnectionString,
    RabbitMQConnectionString,
)
from src.config.exceptions import (
    EmptyValueError,
    EmptyValueErrorMessages,
    InvalidConfigurationError,
)


@pytest.mark.validation
def validate_config(config: dict):
    try:
        match config:
            case {
                "dns": {
                    "timescaledb": timescaledb_config,
                    "eventstoredb": eventstoredb_config,
                    "rabbitmq": rabbitmq_config,
                },
                "ports": ports_config,
                "events": events_config,
                "logging": dict(),
            }:
                # Validate the dns configurations using Pydantic models
                ConnectionStringTimescaleDb(**timescaledb_config)
                EventStoreDBConnectionString(**eventstoredb_config)
                RabbitMQConnectionString(**rabbitmq_config)

                # Validate that ports and events values are not empty strings
                for key, value in ports_config.items():
                    for sub_key, sub_value in value.items():
                        if not sub_value:
                            raise EmptyValueError(
                                f"{EmptyValueErrorMessages.PORTS.value} {key}.{sub_key}"
                            )
                for key, value in events_config.items():
                    for sub_key, sub_value in value.items():
                        if not sub_value:
                            raise EmptyValueError(
                                f"{EmptyValueErrorMessages.EVENTS.value} {key}.{sub_key}"
                            )

            case _:
                raise InvalidConfigurationError(f"Invalid configuration: {config}")

    except ValidationError as e:
        raise InvalidConfigurationError(f"PydanticCustomError: {e}")
