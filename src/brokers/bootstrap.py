from taskiq.cli.worker.args import WorkerArgs
from taskiq.cli.worker.run import run_worker


def start_meals_broker():
    print("Meals broker is running")
    run_worker(
        WorkerArgs(
            broker="src.brokers.meals_broker:meals_broker",
            modules=["src.brokers.meals_broker"],
            workers=3,
        )
    )


def start_health_broker():
    print("Health broker is running")
    run_worker(
        WorkerArgs(
            broker="src.brokers.health_broker:health_broker",
            modules=["src.brokers.health_broker"],
        )
    )
