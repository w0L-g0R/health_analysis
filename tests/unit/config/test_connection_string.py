from pydantic_core import MultiHostUrl
import pytest
from pydantic import ValidationError
from src.config.connection_string import (
    CONNECTION_STRING_MISSING_PARAMETER_ERROR,
    ConnectionStringTimescaleDb,
    # EventStoreDBConnectionString,
    # RabbitMQConnectionString,
    # ConnectionStringMissingParameterError,
)


# def test_resolve_timescale_db_missing_params():
#     with pytest.raises(ValidationError) as exc_info:
#         TimescaleDBConnectionString(host="localhost", port=5432, user="None", )

#     assert "Missing following parameters of timescale_db connection string" in str(
#         exc_info.value
#     )


def test_resolve_timescale_db_success():
    connection = ConnectionStringTimescaleDb(
        user="user",
        password="password",
        host="localhost",
        port="5432",
    )

    assert (
        connection.dns
        == "postgres://user:password@localhost:5432"
    )


def test_uri_in_args_throws_error():
    with pytest.raises(ValidationError) as exc_info:
        uri = MultiHostUrl.build(
            scheme="postgres",
            username="user",
            password="password",
            host="host",
            port=int("1234"),
        )

        ConnectionStringTimescaleDb(
            user="user",
            password="password",
            host="localhost",
            port="5432",
            uri=uri,
        )
    print(exc_info.type)
    assert exc_info.match(
        CONNECTION_STRING_MISSING_PARAMETER_ERROR.message
    )


# def test_resolve_eventstore_db_missing_query_params():
#     with pytest.raises(ConnectionStringMissingParameterError) as exc_info:
#         EventStoreDBConnectionString(host="localhost", port=2113)
#     assert (
#         "Missing following parameters of eventstore_db connection string: query_params"
#         in str(exc_info.value)
#     )


# def test_resolve_eventstore_db_success():
#     resolver = EventStoreDBConnectionString(
#         host="localhost",
#         port=2113,
#         query_params=[("tls", "false")],
#     )
#     assert resolver.uri == "esdb://localhost:2113?tls=false"


# def test_resolve_rabbit_mq_missing_params():
#     with pytest.raises(ConnectionStringMissingParameterError) as exc_info:
#         RabbitMQConnectionString(
#             host="localhost", port=5672, user="test", password="test"
#         )
#     assert "Missing following parameters of rabbit_mq connection string" in str(
#         exc_info.value
#     )


# def test_resolve_rabbit_mq_success():
#     resolver = RabbitMQConnectionString(
#         host="localhost",
#         port=5672,
#         user="user",
#         password="password",
#     )
#     assert resolver.uri == "amqp://user:password@localhost:5672"
