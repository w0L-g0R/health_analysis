def validate_toml_config(config: dict):
    match config:
        case {
            "user": {"player_x": {"color": str()}, "player_o": {"color": str()}},
            "constant": {"board_size": int()},
            "server": {"url": str()},
        }:
            pass
        case _:
            raise ValueError(f"invalid configuration: {config}")
