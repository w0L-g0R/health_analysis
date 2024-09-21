from copy import deepcopy
import logging
from pathlib import Path
from pydantic import ValidationError
import pytest
from toml import load
from src.config.exceptions import (
    EmptyValueError,
    EmptyValueErrorMessages,
    InvalidConfigurationError,
)
from src.config.validation import validate_config

log = logging.getLogger(__name__)

BASE_DIR_PATH = Path.cwd()
CONFIG_FILE_PATH = BASE_DIR_PATH / "src/config/config.toml"


@pytest.fixture
def test_config():
    with open(CONFIG_FILE_PATH, "r") as file:
        return load(file)


@pytest.mark.config_validations
class TestValidation:
    def test_should_throw_when_dns_value_is_missing(self, test_config):
        # ARRANGE
        config = deepcopy(test_config)

        del config["dns"]["timescaledb"]["port"]

        # ACT & ASSERT
        with pytest.raises(InvalidConfigurationError) as exc_info:
            validate_config(config)

        assert "PydanticCustomError" in str(exc_info.value)

    def test_should_throw_when_stream_value_is_empty_string(self, test_config):
        # ARRANGE
        config = deepcopy(test_config)
        config["ports"]["streams"]["meals"] = ""

        # ACT & ASSERT
        with pytest.raises(EmptyValueError) as exc_info:
            validate_config(config)

        assert EmptyValueError(
            f"{EmptyValueErrorMessages.PORTS.value} streams.meals"
        ).message in str(exc_info.value)

    def test_should_throw_when_event_value_is_empty_string(self, test_config):
        # ARRANGE
        config = deepcopy(test_config)

        config["events"]["meals"]["insert"] = ""

        # ACT & ASSERT
        with pytest.raises(EmptyValueError) as exc_info:
            validate_config(config)

        assert EmptyValueError(
            f"{EmptyValueErrorMessages.EVENTS.value} meals.insert"
        ).message in str(exc_info.value)
