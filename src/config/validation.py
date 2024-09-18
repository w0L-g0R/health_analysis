def validate_config(config: dict):
    match config:
        case {
            "user": {"player_x": str()},
            "player_o": {"color": str()},
            "constant": {"board_size": int()},
            "server": {"host": str(), "port": str(), "user": str(), "password": str()},
        }:
            pass
        case _:
            raise ValueError(f"invalid configuration: {config}")
