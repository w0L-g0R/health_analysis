import logging

import pytest

# @pytest.hookimpl(trylast=True)
# def pytest_configure(config):
#     logging_plugin = config.pluginmanager.get_plugin("logging-plugin")

#     # Change color on existing log level
#     logging_plugin.log_cli_handler.formatter.add_color_level(logging.INFO, "cyan")
