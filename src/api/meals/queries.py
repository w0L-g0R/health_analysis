from config import MEALS_TABLE


def get_all_meals() -> str:
    return f"SELECT * from {MEALS_TABLE}"
