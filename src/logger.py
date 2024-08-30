def get_logging_config_from(toml_data: dict) -> dict:
    """
    Convert TOML data to a logging configuration dictionary.

    :param toml_data: The parsed TOML data as a dictionary.
    :return: A dictionary suitable for use with logging.config.dictConfig.
    """
    logging_config = {
        "version": toml_data.get("logging", {}).get(
            "version", 1
        ),
        "formatters": {
            "formatter": {
                "format": toml_data.get("logging", {})
                .get("formatters", {})
                .get("formatter", {})
                .get("format", "")
            }
        },
        "handlers": {},
        "root": {
            "level": toml_data.get("logging", {})
            .get("root", {})
            .get("level", "WARNING"),
            "handlers": toml_data.get("logging", {})
            .get("root", {})
            .get("handlers", []),
        },
    }

    # Map handlers
    for handler in toml_data.get("logging", {}).get(
        "handlers", []
    ):
        handler_type = handler.get("type")
        logging_config["handlers"][handler_type] = {
            "class": handler.get("class"),
            "level": handler.get("level"),
            "formatter": handler.get("formatter"),
            "stream": handler.get("stream"),
        }

    return logging_config
