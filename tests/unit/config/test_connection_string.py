import logging

from pydantic import ValidationError
from pydantic_core import MultiHostUrl
import pytest

from src.config.connection_strings import (
    ConnectionStringTimescaleDb,
    EventStoreDBConnectionString,
    UriPassedToInitError,
)

log = logging.getLogger(__name__)


@pytest.fixture
def params():
    return {
        "scheme": "postgres",
        "user": "user",
        "password": "password",
        "host": "localhost",
        "port": 5432,
    }


@pytest.mark.connection_string
class TestConnectionString:
    def test_should_resolve_timescale_db(self, params):
        # ACT
        connection = ConnectionStringTimescaleDb(
            user=params["user"],
            password=params["password"],
            host=params["host"],
            port=params["port"],
        )

        # ASSERT
        assert (
            connection.dns
            == f"{params['scheme']}://{params['user']}:{params['password']}@{params['host']}:{params['port']}"
        )

    def test_should_resolve_eventstore_db_with_tls(self, params):
        # ACT
        connection = EventStoreDBConnectionString(
            user=params["user"],
            password=params["password"],
            host=params["host"],
            port=params["port"],
            tls=True,
        )

        # ASSERT
        assert (
            connection.dns
            == f"esdb://{params['user']}:{params['password']}@{params['host']}:{params['port']}?tls=true"
        )

    def test_should_resolve_eventstore_db_with_no_tls(self, params):
        # ACT
        connection = EventStoreDBConnectionString(
            user=params["user"],
            password=params["password"],
            host=params["host"],
            port=params["port"],
            tls=False,
        )

        # ASSERT
        assert connection.dns == f"esdb://{params['host']}:{params['port']}?tls=false"

    def test_should_resolve_rabbitmq(self, params):
        # ACT
        connection = ConnectionStringTimescaleDb(
            user=params["user"],
            password=params["password"],
            host=params["host"],
            port=params["port"],
        )
        # ASSERT
        assert (
            connection.dns
            == f"{params['scheme']}://{params['user']}:{params['password']}@{params['host']}:{params['port']}"
        )

    def test_should_throw_when_uri_passed_to_init(self, params):
        # ARRANGE
        uri = MultiHostUrl.build(
            scheme=params["scheme"],
            username=params["user"],
            password=params["password"],
            host=params["host"],
            port=params["port"],
        )

        # ACT
        with pytest.raises(ValidationError) as exc_info:
            ConnectionStringTimescaleDb(
                user=params["user"],
                password=params["password"],
                host=params["host"],
                port=params["port"],
                uri=uri,
            )

        # ASSERT
        assert exc_info.value.errors()[0]["msg"] == UriPassedToInitError.message
        assert exc_info.value.errors()[0]["type"] == UriPassedToInitError.error_type
